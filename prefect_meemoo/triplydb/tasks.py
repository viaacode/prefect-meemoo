import json
import os
import re
import subprocess
import time
from collections import deque

from prefect import get_run_logger, task
from prefect.artifacts import create_markdown_artifact
from prefect.blocks.core import Block, SecretStr
from prefect.states import Failed

# def create_etl_err_artifact(flow, flow_run, state):
#     """
#     Create an artifact with the given filename.
#     """
#     return

@task(
    name="Run TriplyETL",
    description="Runs an TriplyETL script.",
    task_run_name="{task_run_name}",
)
def run_triplyetl(
    etl_script_path: str, task_run_name: str = "Run TriplyETL", base_path = os.getcwd(), **kwargs
):
    logger = get_run_logger()
    # Resolve absolute path of TriplyETL script
    etl_script_abspath = os.path.abspath(etl_script_path)
    logger.info("Running TriplyETL script: " + str(etl_script_abspath))

    # Create an environment for subprocess
    etl_env = os.environ.copy()
    etl_env["BASE_PATH"] = base_path

    # 
    log_queue = deque(maxlen = 30)

    for key, value in kwargs.items():
        # If a prefect block is given, make members available in ENV
        if issubclass(type(value), Block):
            for b_key, b_value in value.dict().items():
                if b_key.startswith("_") or b_value is None:
                    continue
                if isinstance(b_value, SecretStr):
                    etl_env[
                        f"{key.upper()}_{b_key.upper()}"
                    ] = b_value.get_secret_value()
                else:
                    etl_env[f"{key.upper()}_{b_key.upper()}"] = str(b_value)
        elif value is not None:
            etl_env[key.upper()] = str(value)

    p = subprocess.Popen(
        ["npx", "etl", str(etl_script_abspath), "--plain"],
        cwd=os.path.dirname(etl_script_abspath),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        env=etl_env,
        encoding="utf-8",
    )

    record_message = False
    message = ""
    error = False

    # Parse CLI output from TriplyETL for logging
    while True:
        line = p.stdout.readline()
        # Remove ANSI escape sequences
        line = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", line)

        # Push to queue
        if line:
            log_queue.append(line)

        # Break loop when subprocess has ended
        if line == "" and p.poll() is not None:
            if record_message:
                logger.error(message)
            break
        
        if "PREFECT" in line:
            log_statement = json.loads(line)["PREFECT"]
            if log_statement["level"] == "INFO":
                try:
                    if log_statement["message"] == "error":
                        record_message = True
                except KeyError:
                    pass
                logger.info(log_statement)
            elif log_statement["level"] == "WARNING":
                logger.warning(log_statement)
            elif log_statement["level"] == "ERROR":
                logger.error(log_statement)

        if record_message:
            message += line


    # Read final returncode
    rc = p.poll()
    logger.info("rc: " + str(rc))
    if rc > 0:
        logger.error('\n'.join(log_queue))
        try:
            with open(base_path + "lib/etl.err") as f:
                error_message = f.read()
                create_markdown_artifact(
                    error_message,
                    key="etl-err",
                    description=f"TriplyETL Error: {etl_script_path}",
                )
        except FileNotFoundError:
            logger.info("File not found: " + base_path + "lib/etl.err")
        return Failed()

    return rc > 0

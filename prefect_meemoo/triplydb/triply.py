import os
import re
import subprocess
import sys
import time
from pathlib import Path

from prefect import get_run_logger, task
from prefect.blocks.core import Block, SecretStr
from prefect.states import Failed


@task(name="Run TriplyETL", description="Runs an TriplyETL script.")
def run_triplyetl(etl_script_path: str, **kwargs):
    logger = get_run_logger()
    # Resolve absolute path of TriplyETL script
    etl_script_abspath = os.path.abspath(etl_script_path)
    logger.info("Running TriplyETL script: " + str(etl_script_abspath))

    # Create an environment for subprocess
    etl_env = os.environ.copy()
    for key, value in kwargs.items():
        # If a prefect block is given, make members available in ENV
        if issubclass(type(value), Block):
            for b_key, b_value in value.dict().items():
                if b_key.startswith("_"):
                    continue
                if isinstance(b_value, SecretStr):
                    etl_env[f"{key.upper()}_{b_key.upper()}"] = b_value.get_secret_value()
                else:
                    etl_env[f"{key.upper()}_{b_key.upper()}"] = str(b_value)
        else:
            etl_env[key.upper()] = str(value)

    p = subprocess.Popen(
        ["yarn", "etl", str(etl_script_abspath), "--plain"],
        cwd=os.path.dirname(etl_script_abspath),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=etl_env,
        encoding="utf-8",
    )

    # Parse CLI output from TriplyETL for logging

    record_message = False
    message = ""
    prev_statements = ""
    error = False
    last_statement_time = time.time() - 10

    for line in iter(lambda: p.stdout.readline(), ""):
        # # Start recording log message when encountering start frame
        if not line:
            break
        if re.search(r"╭─|┌─", line):
            record_message = True

        # Start recording error message when encountering ERROR
        if re.search(r"ERROR", line):
            record_message = True
            error = True

        if record_message:
            message += line
        # elif bool(line and not line.isspace()):
        #     logger.info(line)

        # Stop recording log message when encountering end frame
        if re.search(r"╰─|└─", line):
            if error:
                logger.error(message)
            else:
                logger.info(message)
            record_message = False
            message = ""
            error = False

        if re.search(r"etl.err", line):
            logger.error(message)
            record_message = False
            message = ""
            error = False
            
        if re.search(r"#Statements:", line):
            if line != prev_statements and time.time() - last_statement_time > 10:          
                logger.info(line)
                prev_statements = line
                last_statement_time = time.time()

    for err in iter(lambda: p.stderr.readlines(), ""):
        if re.match(r"warning", err):
            logger.warning(err)
        else:
            logger.error(err)

    p.wait()

    # Split and log stderr in warning and error
    # for err in p.stderr.readline():
    #     if re.match(r"warning", err):
    #         logger.warning(err)
    #     else:
    #         logger.error(err)
    # logger.info("DONE2")
    if p.returncode > 0:
        return Failed()

    return p.returncode > 0

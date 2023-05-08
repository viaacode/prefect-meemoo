import os
import re
import subprocess
import sys
import time
from pathlib import Path

from prefect import get_run_logger, task
from prefect.blocks.core import Block, SecretStr
from prefect.states import Failed


@task(name="Run TriplyETL", description="Runs an TriplyETL script.", task_run_name="{task_run_name}")
def run_triplyetl(etl_script_path: str, task_run_name: str = "Run TriplyETL", debug=False, **kwargs):
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
                    etl_env[
                        f"{key.upper()}_{b_key.upper()}"
                    ] = b_value.get_secret_value()
                else:
                    etl_env[f"{key.upper()}_{b_key.upper()}"] = str(b_value)
        else:
            etl_env[key.upper()] = str(value)

    p = subprocess.Popen(
        ["yarn", "etl", str(etl_script_abspath), "--plain"],
        cwd=os.path.dirname(etl_script_abspath),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        env=etl_env,
        encoding="utf-8",
    )

    record_message = False
    message = ""
    prev_statements = ""
    error = False
    last_statement_time = time.time() - 10

    # Parse CLI output from TriplyETL for logging
    while True:
        line = p.stdout.readline()
        # Remove ANSI escape sequences
        line = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", line)
        
        # Break loop when subprocess has ended
        if line == "" and p.poll() is not None:
            break

        # Start recording log message when encountering start frame
        if re.search(r"╭─|┌─|ERROR", line):
            record_message = True

        # Set message to error when encountering ERROR
        if re.search(r"ERROR", line):
            error = True
        
        if record_message:
            message += line

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

        if re.search(r"Info", line) and not (re.search(r"Error", line) or re.search(r"Warning", line)) :
            logger.info(line)
            
        if re.search(r"#Statements:", line):
            if line != prev_statements and time.time() - last_statement_time > 10:
                logger.info(line)
                prev_statements = line
                last_statement_time = time.time()

        # The line did not trigger a message, log seperately
        if not record_message and line:
            if re.match(r"warning", line):
                logger.warning(line)
            elif re.match(r"error", line):
                logger.error(line)
            elif debug:
                logger.info(line.strip())

    # Read final returncode
    rc = p.poll()

    if rc > 0:
        return Failed()

    return rc > 0
import os
import re
import subprocess
from pathlib import Path
from prefect.blocks.core import Block, SecretStr

from prefect import get_run_logger, task
from prefect.states import Failed


@task(name="Run TriplyETL", description="Runs an TriplyETL script.")
# task_run_name="triplyetl-{name}-on-{date:%A}")
def run_triplyetl(etl_script_path: str, **kwargs):
    logger = get_run_logger()
    # Resolve absolute path of TriplyETL script
    etl_script_abspath = Path(etl_script_path).resolve()
    logger.info("Running TriplyETL script: " + str(etl_script_abspath))
    etl_folder_abspath = os.path.dirname(etl_script_abspath)
    logger.info("Found TriplyETL folder: " + str(etl_folder_abspath))

    # Create an environment for subprocess
    etl_env = os.environ.copy()
    for key, value in kwargs.items():
        # If a prefect block is given, make members available in ENV
        if issubclass(type(value), Block):
            for b_key, b_value in value.dict().items():
                if isinstance(b_value, SecretStr):
                    etl_env[f"{key.upper()}_{b_key.upper()}"] = b_value.get_secret_value()
                else:
                    etl_env[f"{key.upper()}_{b_key.upper()}"] = b_value
        else:
            etl_env[key.upper()] = str(value)

    p = subprocess.Popen(
        ["yarn", "etl", str(etl_script_abspath)],
        cwd=etl_folder_abspath,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=etl_env,
        encoding="utf-8",
    )

    p.wait()

    # Parse CLI output from TriplyETL for logging
    record_message = False
    error = False
    message = ""
    while True:
        line = p.stdout.readline()

        # Start recording log message when encountering start frame
        if re.search(r"╭─|┌─", line):
            record_message = True

        # Start recording error message when encountering ERROR
        if re.search(r"ERROR", line):
            record_message = True
            error = True

        if record_message:
            message += line
        #elif bool(line and not line.isspace()):
        else:
            logger.info(line)

        # Stop recording log message when encountering end frame
        if re.search(r"╰─|└─", line):
            if error:
                logger.error(message)
            else:
                logger.info(message)
            record_message = False
            error = True
            message = ""

        if not line:
            break

    # Split and log stderr in warning and error
    for err in p.stderr.readlines():
        if re.match(r"warning", err):
            logger.warning(err)
        else:
            logger.error(err)

    if p.returncode > 0:
        return Failed()

    return p.returncode > 0

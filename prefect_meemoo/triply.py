import os
import subprocess
import re
from pathlib import Path

from prefect import get_run_logger, task


@task(name="Run TriplyETL", description="Runs an TriplyETL script.")
# task_run_name="triplyetl-{name}-on-{date:%A}")
def run_triplyetl(etl_script_path: str, **kwargs: str):
    logger = get_run_logger()
    # Resolve absolute path of TriplyETL script
    etl_script_abspath = Path(etl_script_path).resolve()
    etl_folder_abspath = os.path.dirname(etl_script_abspath)

    # Create an environment for subprocess
    etl_env = os.environ.copy()
    for key, value in kwargs.items():
        etl_env[key.upper()] = value
    
    p = subprocess.Popen(
        ["yarn", "ratt", etl_script_abspath],
        cwd=etl_folder_abspath,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=etl_env
    )

    p.wait()

    if p.returncode > 0:
        raise Exception("Running TriplyETL failed.")

    out = p.stdout.read()
    logger.info(out)

    for err in p.stderr.readlines():
        if re.match(r'warning', err):
            logger.warning(err)
        else:
            logger.error(err)

    # while True:
    #     line = p.stdout.readline()
    #     logger.info(repr(line))

    #     if not line:
    #         break

    return p.returncode > 0



import time
from datetime import datetime

import requests
from prefect import get_run_logger, task
from prefect.states import Failed
from requests.exceptions import ConnectionError

STATUS_DELAY = 3

"""
--- General tasks ---
"""


@task(
    name="Run HTTP ETL service",
    description="Runs an ETL service that is exposed by HTTP API.",
)
def sync_etl_service(api_server: str, api_route: str, last_modified: str):
    """
    Task that runs an ETL service over HTTP.

    Args:
        api_server (str): URL of the service
        api_route (str): API route to run
        last_modified (str): A datetime indicating when the ETL was last run

    Returns:
        _type_: _description_
    """
    logger = get_run_logger()
    if last_modified:
        logger.info(f"Start (api_server){api_route} since {last_modified}")
        payload = {
            "full_sync": False,
            # we don't actually need a date here, full sync false is ok
            # 'modified_since': f"{last_modified}T00:00:00"
        }
    else:
        logger.info(f"Start full sync on {api_server}{api_route}")
        payload = {"full_sync": True}

    try:
        res = requests.post(
            f"{api_server}{api_route}",
            headers={"Content-Type": "application/json", "accept": "application/json"},
            json=payload,
        )

        if res.status_code != 200:
            logger.error(f"{api_server}{api_route} sync request failed: {res.text}")
            return Failed()

        running = True
        while running:
            res = requests.get(f"{api_server}{api_route}")
            running = res.json()["job_running"]
            # https://github.com/PrefectHQ/prefect/issues/5635
            # import subprocess
            # subprocess.Popen("prefect flow-run ls >/dev/null", shell=True)
            time.sleep(STATUS_DELAY)

        logger.info(f"{api_server}{api_route} sync completed; Service response: {res.text}")
        return datetime.now()
    except ConnectionError as ce:
        logger.error(f"Connection error {ce}")
        return Failed()

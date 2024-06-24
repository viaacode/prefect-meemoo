import pendulum
from prefect import flow, get_run_logger, task
from prefect.runtime import deployment, flow_run

from .prefect_meemoo.config.last_run import (add_last_run_with_context,
                                             get_last_run_config,
                                             save_last_run_config)


@flow(name="test_last_run_config",  on_completion=[save_last_run_config])
def main_flow():
    logger = get_run_logger()

    last_run = get_last_run_config()
    logger.info(f"last_run: {last_run}")
    assert last_run != None

    context_last_run = get_last_run_config(context="context")
    logger.info(f"context_last_run: {context_last_run}")
    assert context_last_run != None

    context_last_run_2000 = get_last_run_config(format="%Y-%m-%dT%H:%M:%SZ", context="context_2000")
    logger.info(f"context_last_run_2000: {context_last_run_2000}")
    assert context_last_run_2000 == pendulum.datetime(2000, 1, 1, 10).to_iso8601_string()

    add_last_run_with_context("context")
    add_last_run_with_context("context_2000", pendulum.datetime(2000, 1, 1, 10))

    context_last_run_2 = get_last_run_config(context="context")
    logger.info(f"context_last_run_2: {context_last_run_2}")
    assert context_last_run_2 != None
    assert context_last_run_2 > context_last_run




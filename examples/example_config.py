from prefect import flow, get_run_logger

from prefect_meemoo.config.last_run import (get_last_run_config,
                                            save_last_run_config)

# last_run_config example

@flow(name="last_modified_config", on_completion=[save_last_run_config])
def last_modified_config(
    full_sync: bool = False,
):
    """
    Example:
        Configure a flow to save the last run config:
        ```python
        @flow(name="prefect_flow_test", on_completion=[save_last_run_config])
        def last_modified_config(
            full_sync: bool = False,
        ):
            logger = get_run_logger()
            logger.info(get_last_run_config())
            date = get_last_run_config()
        ```
    """
    logger = get_run_logger()
    logger.info("test")
    logger.info(get_last_run_config())
    date = get_last_run_config()


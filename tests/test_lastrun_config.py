from datetime import datetime
from unittest import mock

import pytest
from prefect import flow, get_run_logger
from prefect.testing.utilities import prefect_test_harness

from prefect_meemoo.config.last_run import (get_last_run_config,
                                            save_last_run_config)


def test_last_config():
    @flow(on_completion=[save_last_run_config])
    def last_config_flow():
        logger = get_run_logger()
        logger.info("test")
        logger.info(get_last_run_config())
        date = get_last_run_config("%Y-%m-%d")
        return date
    with prefect_test_harness():
        assert last_config_flow() == None
        assert last_config_flow() == datetime.today().strftime("%Y-%m-%d")


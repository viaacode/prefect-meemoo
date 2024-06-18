from datetime import datetime
from time import sleep
from unittest import mock

import pytest
from prefect import flow, get_run_logger
from prefect.runtime import flow_run
from prefect.testing.utilities import prefect_test_harness

from prefect_meemoo.config.blocks import LastRunConfig
from prefect_meemoo.config.last_run import (add_last_run_with_context,
                                            get_last_run_config,
                                            save_last_run_config)


def test_last_config():
    @flow(name = 'last_config_flow', on_completion=[save_last_run_config])
    def last_config_flow():
        print(flow_run.get_scheduled_start_time().to_iso8601_string())
        logger = get_run_logger()
        logger.info("test")
        logger.info(get_last_run_config())
        date = get_last_run_config("%Y-%m-%d")
        try:
            last_run_config: LastRunConfig = LastRunConfig.load('last-config-flow-lastmodified')
            print(last_run_config.last_run)
            print(last_run_config.last_run_dict)
        except ValueError:
            pass
        date_context = get_last_run_config("%Y-%m-%d", "Date")
        add_last_run_with_context("Date")
        sleep(10)
        return date, date_context
    with prefect_test_harness():
        assert last_config_flow() == (None, None)
        assert last_config_flow() == (datetime.today().strftime("%Y-%m-%d"), datetime.today().strftime("%Y-%m-%d"))
        assert last_config_flow() == (datetime.today().strftime("%Y-%m-%d"), datetime.today().strftime("%Y-%m-%d"))


def test_add_last_config():
    @flow(name = 'add_last_config_flow', on_completion=[save_last_run_config])
    def add_last_config_flow(context: str):
        logger = get_run_logger()
        logger.info("test")
        logger.info(get_last_run_config())
        date = get_last_run_config()
        try:
            last_run_config: LastRunConfig = LastRunConfig.load('add-last-config-flow-lastmodified')
            print(last_run_config.last_run)
            print(last_run_config.last_run_dict)
        except ValueError:
            pass
        date_context = get_last_run_config(context=context)
        add_last_run_with_context(context)
        return date, date_context
    with prefect_test_harness():
        test1 =  add_last_config_flow("1")
        print(test1)
        test2 =  add_last_config_flow("2") 
        print(test2)
        test2 =  add_last_config_flow("2") 
        print(test2)
        test3 =  add_last_config_flow("3") 
        print(test3)



def test_register_block_outside_run():
    with prefect_test_harness():
        last_run_block = LastRunConfig(flow_name="test", name="test-lastmodified")
        last_run_block.save("test-lastmodified", overwrite=True)
        print(last_run_block.get_last_run())
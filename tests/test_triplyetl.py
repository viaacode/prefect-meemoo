import pytest
from prefect import flow
from prefect_meemoo.triply import run_triplyetl


def test_run_triplyetl():
    @flow(name="prefect_flow_triplyetl")
    def test_flow():
        run_triplyetl(etl_script_path="./tests/etl/dist/index.js")

    result = test_flow()
    assert result


def test_run_triplyetl_with_variables():
    @flow(name="prefect_flow_triplyetl_variables")
    def test_flow():
        run_triplyetl(
            etl_script_path="./tests/etl/dist/variables.js", TEST="test-value"
        )

    result = test_flow()
    assert result


def test_run_triplyetl_with_error():
    @flow(name="prefect_flow_triplyetl_error")
    def test_flow():
        run_triplyetl(etl_script_path="./tests/etl/dist/error.js")

    with pytest.raises(Exception) as e_info:
        result = test_flow()

from prefect import flow

from prefect_meemoo.triply import (
    run_triplyetl
)
    

def test_run_triplyetl():
    @flow(name="prefect_flow_triplyetl")
    def test_flow():
        run_triplyetl(etl_folder_path="./tests/etl", etl_script_path="./tests/etl/dist/index.js")

    result = test_flow()

    assert result
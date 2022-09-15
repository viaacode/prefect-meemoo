from prefect import flow

from prefect_meemoo.tasks import (
    goodbye_prefect_meemoo,
    hello_prefect_meemoo,
)


def test_hello_prefect_meemoo():
    @flow
    def test_flow():
        return hello_prefect_meemoo()

    result = test_flow()
    assert result == "Hello, prefect-meemoo!"


def goodbye_hello_prefect_meemoo():
    @flow
    def test_flow():
        return goodbye_prefect_meemoo()

    result = test_flow()
    assert result == "Goodbye, prefect-meemoo!"

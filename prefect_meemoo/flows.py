"""This is an example flows module"""
from prefect import flow

from prefect_meemoo.blocks import MeemooBlock
from prefect_meemoo.tasks import (
    goodbye_prefect_meemoo,
    hello_prefect_meemoo,
)


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    MeemooBlock.seed_value_for_example()
    block = MeemooBlock.load("sample-block")

    print(hello_prefect_meemoo())
    print(f"The block's value: {block.value}")
    print(goodbye_prefect_meemoo())
    return "Done"


if __name__ == "__main__":
    hello_and_goodbye()

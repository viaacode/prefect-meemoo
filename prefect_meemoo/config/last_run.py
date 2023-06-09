from prefect.runtime import deployment, flow_run
from prefect.server.schemas.core import Flow, FlowRun

from prefect_meemoo.config.blocks import LastRunConfig


def save_last_run_config(flow: Flow, flow_run: FlowRun, state):
    """
    Save the last run config for a flow.

    Result:
        The last run config is saved in a block in the prefect server.
        The name of the block is the name of the deployment + "-lastmodified".

    Example:
        Configure a flow to save the last run config:
        ```python
        @flow(name="prefect_flow_test", on_completion=[save_last_run_config])
        def main_flow(
            full_sync: bool = False,
        ):
            logger = get_run_logger()
            logger.info("test")
            logger.info(get_last_run_config())
        ```
    """
    name = deployment.get_name()
    if not name:
        name = flow.name
    name += "-lastmodified"
    name = name.replace("_", "-")
    print(name)
    try:
        last_run_config: LastRunConfig = LastRunConfig.load(name)
        last_run_config.save(name=name, overwrite=True)
    except ValueError:
        last_run_config = LastRunConfig(flow_name=flow.name)
        last_run_config.save(name=name, overwrite=True)

def get_last_run_config(format = "%Y-%m-%dT%H:%M:%S.%fZ"):
    """
    Get the last run config for a flow.
    If the flow is run with the parameter `full_sync` and it is True, the last run config is ignored.

    Arguments:
        format (str): format of the returned timestamp
    Returns:
        The datetime of the last run config or None if no last run config is found.
    
    Example:
        Configure a flow to get the last run config:
        ```python
        @flow(name="prefect_flow_test", on_completion=[save_last_run_config])
        def main_flow(
            full_sync: bool = True,
        ):
            logger = get_run_logger()
            logger.info("test")
            logger.info(get_last_run_config())
        ```
    """
    name = deployment.get_name()
    if not name:
        name = flow_run.get_flow_name()
    name += "-lastmodified"
    name = name.replace("_", "-")
    print(name)
    flow_run_parameters = flow_run.get_parameters()
    print(flow_run_parameters)
    if "full_sync" in flow_run_parameters:
        if flow_run_parameters["full_sync"]:
            return None
    try:
        last_run_config: LastRunConfig = LastRunConfig.load(name)
        return last_run_config.get_last_run(format)
    except ValueError as e:
        print(e)
        return None
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
    last_run_config = _get_current_last_run_config(name)
    if not last_run_config:
        last_run_config: LastRunConfig = LastRunConfig(flow_name=flow.name, name = name)
    last_run_config.add_last_run(time=flow_run.start_time)

def _get_current_last_run_config_name(name=None) -> str:
    name = deployment.get_name()
    if not name:
        name = flow_run.get_flow_name()
    name += "-lastmodified"
    return name.replace("_", "-")
    
def _get_current_last_run_config(name=None) -> LastRunConfig: 
    if not name:
        name = _get_current_last_run_config_name()
    try:
        return LastRunConfig.load(name)
    except ValueError as e:
        return None

def add_last_run_with_context(context):
    name = _get_current_last_run_config_name()
    last_run_config = _get_current_last_run_config(name)
    if not last_run_config:
        last_run_config: LastRunConfig = LastRunConfig(flow_name=flow_run.get_flow_name(), name=name)
    last_run_config.add_last_run(context)

def get_last_run_config(format = "%Y-%m-%dT%H:%M:%S.%fZ", context: str = ""):
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
    flow_run_parameters = flow_run.get_parameters()
    if "full_sync" in flow_run_parameters:
        if flow_run_parameters["full_sync"]:
            return None
    last_run_config = _get_current_last_run_config()
    if last_run_config:
        return last_run_config.get_last_run(format, context)
    else:
        return None
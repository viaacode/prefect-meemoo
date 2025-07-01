from prefect import task, get_run_logger
from prefect.client.orchestration import get_client
from prefect.client.schemas.objects import StateType
from prefect.deployments import run_deployment
from prefect._internal.concurrency.api import create_call, from_sync
from pydantic import BaseModel, AnyUrl

class deploymentModel(BaseModel):
    """
    Represents a deployment with its name, active status, and URL.
    """
    name: str
    active: bool = True
    url: AnyUrl = None

class downstreamDeploymentModel(deploymentModel):
    """
    Represents a downstream deployment with its name, active status, URL, and boolean for ready for updates.
    """
    ready: bool = True

@task(task_run_name="Run deployment {name}")
def run_deployment_task(
    name: str,
    as_subflow: bool = True
):
    logger = get_run_logger()
    logger.info(f"Running deployment {name}")
    flow_run = run_deployment(
        name=name,
        as_subflow=as_subflow
    )
    if as_subflow and flow_run.state.type != StateType.COMPLETED:
        logger.error(f"Deployment {name} failed")
        logger.error(flow_run.state.message)
        raise Exception(f"Deployment {name} failed")

@task(task_run_name="Change deployment parameters {name}")
def change_deployment_parameters(
    name: str,
    parameters: dict
):
    """
    Change the parameters of a deployment.
    """
    logger = get_run_logger()
    logger.info(f"Changing deployment {name} parameters to {parameters}")
    prefect_client = get_client()
    deployment = from_sync.call_soon_in_loop_thread(
        create_call(prefect_client.read_deployment_by_name, name)
    ).result()
    logger.info(f"Current parameters: {deployment.parameters}")
    for key, value in parameters.items():
        if key not in deployment.parameters:
            logger.warning(f"Parameter {key} not found in deployment {name}")
            continue
        deployment.parameters[key] = value
    from_sync.call_soon_in_loop_thread(
        create_call(prefect_client.update_deployment, deployment)
    )
    return

async def task_failure_hook_change_deployment_parameters(
    task, task_run, state, **kwargs
):
    """
    Hook to change deployment parameters on task failure.
        - **kwargs:
            - `name`: The name of the deployment.
            - `parameters`: A dictionary of parameters to change.
    """
    logger = get_run_logger()
    for key, value in kwargs:
        if key == "name" and value:
            name = value
        elif key == "parameters" and isinstance(value, dict):
            parameters = value
        elif key == "name" and not value:
            logger.error("'name' of deployement is required in kwargs.")
            raise ValueError("'name' of deployement is required in kwargs.")
        elif key == "parameters" and not isinstance(value, dict):
            logger.error("Parameters must be a dictionary.")
            raise ValueError("Parameters must be a dictionary.")
        else:
            logger.error(f"Invalid kwarg {key}. Only 'name' and 'parameters' are allowed.")
            raise ValueError(f"Invalid kwarg {key}. Only 'name' and 'parameters' are allowed.")
        
    logger = get_run_logger()
    logger.info(f"Changing deployment {name} parameters to {parameters}")
    prefect_client = get_client()
    deployment = await prefect_client.read_deployment_by_name(name)
    for key, value in parameters.items():
        if key not in deployment.parameters:
            logger.warning(f"Parameter {key} not found in deployment {name}")
            continue
        deployment.parameters[key] = value
    await prefect_client.update_deployment(deployment)

@task(task_run_name="Get current deployment parameter from {name}")
def get_deployment_parameter(name: str, parameter_name: str) -> dict:
    """
    Get the current value of a deployment parameter.
    """
    logger = get_run_logger()
    logger.info(f"Getting current value for parameter {parameter_name} from deployment {name}")
    prefect_client = get_client()
    # deployment = await prefect_client.read_deployment_by_name(name)
    deployment = from_sync.call_soon_in_loop_thread(
        create_call(prefect_client.read_deployment_by_name, name)
    ).result()
    if parameter_name not in deployment.parameters:
        logger.warning(f"Parameter {parameter_name} not found in deployment {name}")
        return None
    return deployment.parameters[parameter_name]

@task(task_run_name="Mark deployment {name} as ready for updates in upstream deployment {upstream_name}")
def mark_deployment_as_ready(
    name: str,
    upstream_name: str,
    downstream_deployment_parameter: str
):
    """
    Mark a deployment as ready for updates in an upstream deployment.
    """
    logger = get_run_logger()
    logger.info(f"Marking deployment {name} as ready for updates in upstream deployment {upstream_name}")
    downstream_deployment = get_deployment_parameter.fn(name=upstream_name, parameter_name=downstream_deployment_parameter)
    if not downstream_deployment:
        logger.error(f"Downstream deployment parameter {downstream_deployment_parameter} not found in upstream deployment {upstream_name}")
        raise ValueError(f"Downstream deployment parameter {downstream_deployment_parameter} not found in upstream deployment {upstream_name}")
    elif isinstance(downstream_deployment, list):
        for deployment in downstream_deployment:
            if deployment.name == name:
                deployment.ready = True
                logger.info(f"Deployment {name} marked as ready for updates")
                break
        else:
            logger.error(f"Deployment {name} not found in downstream deployments of {upstream_name}")
            raise ValueError(f"Deployment {name} not found in downstream deployments of {upstream_name}")
    elif isinstance(downstream_deployment, dict):
        if downstream_deployment.name == name:
            downstream_deployment.ready = True
            logger.info(f"Deployment {name} marked as ready for updates")
    else:
        logger.error(f"Downstream deployment parameter {downstream_deployment_parameter} is not a valid deployment model in upstream deployment {upstream_name}")
        raise ValueError(f"Downstream deployment parameter {downstream_deployment_parameter} is not a valid deployment model in upstream deployment {upstream_name}")
    # Update the upstream deployment with the modified downstream deployment
    change_deployment_parameters.fn(name=upstream_name, parameters={downstream_deployment_parameter: downstream_deployment})

@task(task_run_name="Mark deployment {name} as not ready for updates in upstream deployment {upstream_name}")
def mark_deployment_as_not_ready(
    name: str,
    upstream_name: str,
    downstream_deployment_parameter: str
):
    """
    Mark a deployment as not ready for updates in an upstream deployment.
    """
    logger = get_run_logger()
    logger.info(f"Marking deployment {name} as not ready for updates in upstream deployment {upstream_name}")
    downstream_deployment = get_deployment_parameter.fn(name=upstream_name, parameter_name=downstream_deployment_parameter)
    if not downstream_deployment:
        logger.error(f"Downstream deployment parameter {downstream_deployment_parameter} not found in upstream deployment {upstream_name}")
        raise ValueError(f"Downstream deployment parameter {downstream_deployment_parameter} not found in upstream deployment {upstream_name}")
    elif isinstance(downstream_deployment, list):
        for deployment in downstream_deployment:
            if deployment.name == name:
                deployment.ready = False
                logger.info(f"Deployment {name} marked as not ready for updates")
                break
        else:
            logger.error(f"Deployment {name} not found in downstream deployments of {upstream_name}")
            raise ValueError(f"Deployment {name} not found in downstream deployments of {upstream_name}")
    elif isinstance(downstream_deployment, dict):
        if downstream_deployment.name == name:
            downstream_deployment.ready = False
            logger.info(f"Deployment {name} marked as not ready for updates")
    else:
        logger.error(f"Downstream deployment parameter {downstream_deployment_parameter} is not a valid deployment model in upstream deployment {upstream_name}")
        raise ValueError(f"Downstream deployment parameter {downstream_deployment_parameter} is not a valid deployment model in upstream deployment {upstream_name}")
    # Update the upstream deployment with the modified downstream deployment
    change_deployment_parameters.fn(name=upstream_name, parameters={downstream_deployment_parameter: downstream_deployment})
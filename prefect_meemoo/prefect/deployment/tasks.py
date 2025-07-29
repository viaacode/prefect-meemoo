import requests
from prefect import task, get_run_logger
from prefect.client.orchestration import get_client
from prefect.client.schemas.objects import StateType
from prefect.deployments import run_deployment
from prefect._internal.concurrency.api import create_call, from_sync
from prefect_meemoo.prefect.deployment.models import SubDeploymentModel, DeploymentModel, is_deployment_model
from typing import Union

@task(task_run_name="Run deployment {name}")
def run_deployment_task(
    name: str,
    as_subflow: bool = True
):
    """
    Run a deployment by its name.
    If `as_subflow` is True, it will run the deployment as a subflow.
    If `as_subflow` is False, it will run the deployment as a flow run, not waiting for its completion.
    """
    logger = get_run_logger()
    logger.info(f"Running deployment {name}")
    flow_run = run_deployment(
        name=name,
        as_subflow=as_subflow,
        timeout=0 if not as_subflow else None
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
def get_deployment_parameter(name: str, parameter_name: str):
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

@task(task_run_name="Check if downstream deployments or its sub-deployments are blocking")
def check_deployment_blocking(
    deployment_model: Union[SubDeploymentModel, DeploymentModel, list[SubDeploymentModel], list[DeploymentModel]]
) -> bool:
    """
    Check if a deployment or its sub-deployments are blocking.
    """
    logger = get_run_logger()

    if isinstance(deployment_model, list):
        for dep in deployment_model:
            if check_deployment_blocking.fn(dep):
                return True
        return False
    
    if deployment_model.is_blocking:
        logger.info(f"Checking if downstream deployment {deployment_model.name} or its sub-deployments are blocking")
        if check_deployment_running_flows(deployment_model.name):
            logger.info(f"Deployment {deployment_model.name} is blocking new flow run.")
            return True
        
    if not isinstance(deployment_model, DeploymentModel):
        return False
    
    for sub_deployment in deployment_model.sub_deployments:
        if check_deployment_blocking(sub_deployment):
            logger.info(f"Sub-deployment {sub_deployment.name} is blocking new flow run.")
            return True
    return False

@task(task_run_name="Add sub-deployments to deployment.")
def setup_sub_deployments_to_deployment_parameter(
    name: str,
    deployment_model: Union[DeploymentModel, list[DeploymentModel]],
    deployment_model_parameter: str
) -> bool:
    """
    Add sub-deployments to a downstream deployment.

    Args:
        name (str): The name of the deployment.
        deployment_model (DeploymentModel): The downstream deployment model to which sub-deployments will be added.
        deployment_model_parameter (str): The parameter name of the deployment where sub-deployments will be added.

    Returns:
        Bool: True if sub-deployments were added, False otherwise.
    """
    logger = get_run_logger()
    prefect_client = get_client()
    has_added = False

    if isinstance(deployment_model, list):
        for deployment in deployment_model:
            has_added = has_added or setup_sub_deployments_to_deployment_parameter(
                name=name,
                deployment_model=deployment,
                deployment_model_parameter=deployment_model_parameter
            )
        return has_added
    
    logger.info(f"Adding sub-deployments to downstream deployment {deployment_model.name}")
    downstream_deployment = from_sync.call_soon_in_loop_thread(
        create_call(prefect_client.read_deployment_by_name, deployment_model.name)
    ).result()
    logger.info(downstream_deployment.parameters)
    for key, value in downstream_deployment.parameters.items():
        if is_deployment_model(value):
            deployment = DeploymentModel(**value)
            if deployment.name not in [d.name for d in deployment_model.sub_deployments]:
                sub_deployment = SubDeploymentModel(
                    name=deployment.name,
                    active=deployment.active,
                    is_blocking=deployment.is_blocking,
                    full_sync=deployment.full_sync
                )
                deployment_model.sub_deployments.append(sub_deployment)
                has_added = True
                logger.info(f"Added sub-deployment {deployment.name} to downstream deployment {deployment_model.name}, check if it is blocking.")
    if has_added:
        current_deployment_parameters = get_deployment_parameter.fn(
            name=name,
            parameter_name=deployment_model_parameter
        )
        if isinstance(current_deployment_parameters, list):
            for current_deployment_model in current_deployment_parameters:
                if not is_deployment_model(current_deployment_model):
                    logger.error(f"Current deployment parameter {deployment_model_parameter} is not a DeploymentModel.")
                    raise ValueError(f"Current deployment parameter {deployment_model_parameter} is not a DeploymentModel.")
                if current_deployment_model["name"] == deployment_model.name:
                    current_deployment_model["sub_deployments"] = deployment_model.sub_deployments
                    change_deployment_parameters.fn(
                        name=name,
                        parameters={
                            deployment_model_parameter: [dep for dep in current_deployment_parameters]
                        }
                    )
                    break
        else:
            change_deployment_parameters.fn(
                name=name,
                parameters={
                    deployment_model_parameter: deployment_model.dict()
                }
            )
    return has_added

@task(task_run_name="Change downstream sub-deployment parameters {deployment_model.name}")
def propagate_sub_deployment_parameters(
    deployment_model: DeploymentModel,
):
    """
    Change parameters of sub-deployments in a downstream deployment.
    Args:
        downstream_deployment_model (DeploymentModel): The downstream deployment model containing sub-deployments.
    """
    logger = get_run_logger()
    downstream_deployment = from_sync.call_soon_in_loop_thread(
        create_call(get_client().read_deployment_by_name, deployment_model.name)
    ).result()
    for key, value in downstream_deployment.parameters.items():
        has_changed = False
        if is_deployment_model(value):
            deployment = DeploymentModel(**value)
            for sub_deployment in deployment_model.sub_deployments:
                if sub_deployment.name == deployment.name:
                    has_changed = sub_deployment.active != deployment.active or \
                        sub_deployment.full_sync != deployment.full_sync
                    deployment.active = sub_deployment.active
                    deployment.full_sync = sub_deployment.full_sync
                if has_changed:
                    logger.info(f"Changing parameters of sub-deployments in downstream deployment {deployment_model.name}")
                    change_deployment_parameters.fn(
                        name=deployment_model.name,
                        parameters={
                            key: deployment.dict()
                        }
                    )
                    break

@task(task_run_name="Toggle deployment parameter active status")
def toggle_deployment_parameter_active(
    name: str,
    deployment_model_parameter: str,
) -> bool:
    """
    Toggle the active status of a deployment parameter.
    Args:
        name (str): The name of the deployment.
        deployment_model_parameter (str): The parameter name of the deployment to toggle.
    Returns:
        bool: True if the active status was toggled, False otherwise.
    """
    logger = get_run_logger()
    prefect_client = get_client()
    deployment = from_sync.call_soon_in_loop_thread(
        create_call(prefect_client.read_deployment_by_name, name)
    ).result()
    
    if deployment_model_parameter not in deployment.parameters:
        logger.warning(f"Parameter {deployment_model_parameter} not found in deployment {name}")
        return False
    
    current_value = deployment.parameters[deployment_model_parameter]
    
    if not is_deployment_model(current_value):
        logger.error(f"Parameter {deployment_model_parameter} is not a DeploymentModel.")
        raise ValueError(f"Parameter {deployment_model_parameter} is not a DeploymentModel.")
    
    deployment_model = DeploymentModel(**current_value)
    deployment_model.active = not deployment_model.active
    change_deployment_parameters.fn(
        name=name,
        parameters={
            deployment_model_parameter: deployment_model.dict()
        }
    )
    
    logger.info(f"Toggled active status of parameter {deployment_model_parameter} in deployment {name} to {deployment_model.active}")
    return True

def check_deployment_running_flows(
    name: str,
    max_running: int = 0
) -> bool:
    """
    This function returns a list of all running flow runs for a given flow name in Prefect.
    Args:
        name (str): The name of the deployment.
        max_running (int): The maximum number of running flow runs to check for. If 0, it will return True if there are any running flow runs.
    Returns:
        bool: True if there are running flow runs, False otherwise.
    """
    prefect_client = get_client()
    deployment = from_sync.call_soon_in_loop_thread(
        create_call(prefect_client.read_deployment_by_name, name)
    ).result()
    url = f"{prefect_client.api_url}flow_runs/filter"
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "flow_runs" : {
            "state": {
                "type" : {
                    "any_": ["RUNNING"]
                }
            }
        },
        "deployments" : {
            "id" : {
                "any_": [str(deployment.id)]
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    flow_runs = response.json()
    if flow_runs and len(flow_runs) > max_running:
        logger = get_run_logger()
        logger.info(f"Deployment {name} has running flow runs: {', '.join([flow_run['id'] for flow_run in flow_runs])}")
        return True
    else:
        logger = get_run_logger()
        logger.info(f"Deployment {name} has no running flow runs")
        return False

def check_deployment_last_flow_run_failed(
    name: str,
    last_n: int = 1
) -> bool:
    """
    Check if the last N flow runs of a deployment have failed.
    Args:
        name (str): The name of the deployment.
        last_n (int): The number of last flow runs to check for failures.
    Returns:
        bool: True if any of the last N flow runs have failed, False otherwise.
    """
    prefect_client = get_client()
    deployment = from_sync.call_soon_in_loop_thread(
        create_call(prefect_client.read_deployment_by_name, name)
    ).result()
    url = f"{prefect_client.api_url}flow_runs/filter"
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "sort" : "START_TIME_DESC",
        "limit": last_n,
        "deployments" : {
            "id" : {
                "any_": [str(deployment.id)]
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)

    flow_runs = response.json()
    if flow_runs and any(
        flow_run["state_type"] == "FAILED" for flow_run in flow_runs
    ):
        logger = get_run_logger()
        logger.info(f"Deployment {name} has failed flow runs: {', '.join([flow_run['id'] for flow_run in flow_runs if flow_run['state_type'] == 'FAILED'])}")
        return True
    else:
        logger = get_run_logger()
        logger.info(f"Deployment {name} has no failed flow runs")
        return False
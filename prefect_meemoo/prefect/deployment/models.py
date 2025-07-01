from pydantic import BaseModel, AnyUrl

class SubDeploymentModel(BaseModel):
    """
    Represents a sub-deployment
    with its name, active status, URL, and boolean for ready for updates.
    """
    name: str
    active: bool = True
    is_blocking: bool = False
    full_sync: bool = False

class DeploymentModel(BaseModel):
    """
    Represents a deployment with its name, active status, and URL.
    If `is_blocking` is True, the deployment is blocking a next flow run of the parent deployment.
    """
    name: str
    active: bool = True
    is_blocking: bool = False
    full_sync: bool = False
    sub_deployments: list[SubDeploymentModel] = []

def is_sub_deployment_model(obj: dict) -> bool:
    """
    Check if the dict can be converted to an instance of DeploymentModel.
    """
    try:
        SubDeploymentModel(**obj)
        return True
    except Exception:
        return False
    
from pydantic import BaseModel, AnyUrl

class deploymentModel(BaseModel):
    """
    Represents a deployment with its name, active status, and URL.
    """
    name: str
    active: bool = True
    full_sync: bool = False
    url: AnyUrl = None

class downstreamDeploymentModel(deploymentModel):
    """
    Represents a downstream deployment with its name, active status, URL, and boolean for ready for updates.
    """
    ready: bool = True
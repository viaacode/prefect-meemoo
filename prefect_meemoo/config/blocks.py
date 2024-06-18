import pendulum
from dateutil import parser
from prefect.blocks.core import Block, SecretStr
from prefect.runtime import flow_run
from pydantic import Field


class LastRunConfig(Block):
    """
    Block used to manage the configuration of when a flow last ran (the day).
    
    Attributes:
        last_run: The last time the flow ran.
        flow_name: The name of the flow.

    Example:
        Load stored LastRun configuration:
        ```python
        from prefect_meemoo.blocks import LastRunConfig
        LastRun = LastRunConfig.load("BLOCK_NAME")
        last_run = LastRun.last_run
        ```
    """

    _block_type_name = "Last Run Config"
    _logo_url = "https://cdn-icons-png.flaticon.com/512/8766/8766995.png"
    last_run: str = Field(default=flow_run.get_scheduled_start_time().to_iso8601_string(), description="The last time the flow started.")
    last_run_dict: dict = Field({}, description="Dictionary containing dates based on a certain value for a flow.")
    flow_name: str = Field(default=(...), description="The name of the flow.")
    name: str = Field(default=(...), description="The name of the deployment.")
    _block_schema_capabilities = ["meemoo-prefect", "config"]

    def get_last_run(self, format: str = "%Y-%m-%dT%H:%M:%S.%fZ", context: str = ""):
        if context:
            try:
                return parser.parse(self.last_run_dict[context]).strftime(format)
            except KeyError:
                return None
        return parser.parse(self.last_run).strftime(format)

    def add_last_run(self, context: str = "", time: pendulum.DateTime= None):
        if context:
            if not time:
                self.last_run_dict[context] = flow_run.get_scheduled_start_time().to_iso8601_string()
            else:
                self.last_run_dict[context] = time.to_iso8601_string()
        else:
            if not time:
                self.last_run = flow_run.get_scheduled_start_time().to_iso8601_string()
            else:
                self.last_run = time.to_iso8601_string()
        self.save(name=self.name, overwrite=True)
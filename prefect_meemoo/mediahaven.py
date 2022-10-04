import json
from typing import List, Tuple
import time

from prefect import task, flow, get_run_logger
from prefect.blocks.system import Secret, JSON, String


from mediahaven import MediaHaven
from mediahaven.mediahaven import MediaHavenException
from mediahaven.oauth2 import ROPCGrant, RequestTokenError

'''
--- Tasks ---
'''

@task
def update_metadata(client: MediaHaven, fragment_id, xml=None, json=None) -> bool:
    time.sleep(1)
    logger = get_run_logger()
    resp = None
    try:
        resp = client.records.update(record_id=fragment_id, json=json, xml=xml)
        logger.info(f"Updated: {fragment_id}")
        return resp
    except Exception as e:
        logger.warning(e)
        logger.warning("Not updated: " + fragment_id)
        return resp

@task()
def generate_mediahaven_json(client : MediaHaven, field_value: List[Tuple[str, str]]) -> dict:
    '''
    Generate a json object that can be used to update metadata in MediaHaven
    Parameters:
        - client: MediaHaven client
        - field_value: List of tuples with field name and value
    Returns:
        - json object  
    '''
    logger = get_run_logger()
    # Get the field definitions block
    try:
        field_definitions = JSON.load("mediahaven-field-definitions")
    except ValueError as e:
        field_definitions = {}
    # Save the field definition in JSON block if it is not there yet
    if field not in field_definitions:
        field_definitions[field] = get_field_definition.fn(client, field)
        try:
            JSON(value=field_definitions).save("mediahaven-field-definitions", overwrite=True)
        except Exception as e:
            logger.error(f"Error saving metadata structure: {e}")
            raise Exception(f"Error saving JSON block: {e}")
    # Generate the JSON
    json_dict = {'Metadata': {}}
    for field, value in field_value:
        if field_definitions[field]["Family"] not in json_dict["Metadata"]:
            json_dict['Metadata'][field_definitions[field]["Family"]]= {field : value}
        else:
            json_dict['Metadata'][field_definitions[field]["Family"]][field] = value
    return json_dict

@task()
def get_field_definition(client : MediaHaven, field: str) -> dict:
    field_description = {}
    field_dict = json.loads(client.fields.get(field=field).raw_response)
    field_description["Family"] = field_dict["Family"]
    field_description["Type"] = field_dict["Type"]
    return field_description

@task()
def single_value_metadata_update(client : MediaHaven, fragment_id: str, field: str, value,) -> bool:
    '''
    Update a single value in MediaHaven
    Parameters:
        - client: MediaHaven client
        - fragment_id: MediaHaven fragment id
        - field: MediaHaven field name
        - value: Value to update
    Returns:
        - True if the update was successful, False otherwise
    '''
    # Get Prefect logger
    logger = get_run_logger()
    # Get JSON format for MediaHaven metadata update
    json_dict = generate_mediahaven_json.fn(client, [(field, value)])
    # Update metadata
    resp = update_metadata.fn(client, fragment_id, json=json_dict)
    return resp

'''
--- Flows ---
'''

@flow(name="mediahaven-update-single-record-flow")
def main_flow(fragment_id: str, field: str, value, ):
    """
    Flow to update metadata in MediaHaven.
    Parameters:
        - fragment_id: ID of the record to update
        - field: Name of the field to update
        - value: Value of the field to update
    Blocks:
        - Mediahaven endpoint in String Block in Prefect (https)
        - MediaHaven account with access to the endpoint
        - Client ID and Client Secret for the MediaHaven account in Secret Blocks in Prefect
        - Username and password for the MediaHaven account in Secret Blocks in Prefect

    """
    # Get the MediaHaven endpoint
    endpoint = String.load("mediahaven-prd-endpoint")
    # Get OAuth2 Client and request token
    grant = ROPCGrant(endpoint, Secret.load("mediahaven-prd-client-id").get(), Secret.load("mediahaven-prd-client-secret").get())
    grant.request_token(Secret.load("mediahaven-prd-user").get(), Secret.load("mediahaven-prd-password").get())
    # Create MediaHaven client
    client = MediaHaven(endpoint, grant)
    # Update metadata
    resp = single_value_metadata_update(client, fragment_id, field, value)

    


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
    '''
    Update metadata of a fragment.

    Parameters:
        - client: MediaHaven client
        - fragment_id: ID of the fragment to update
        - xml: XML metadata to update
        - json: JSON metadata to update

    Returns:
        - True if the metadata was updated, False otherwise
    '''
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
        field_definitions = JSON.load("mediahaven-field-definitions").value
    except ValueError as e:
        field_definitions = {}
    # Generate the JSON
    json_dict = {'Metadata': {}}
    for field, value in field_value:
        # Save the field definition in JSON block if it is not there yet
        if field not in field_definitions:
            field_definitions[field] = get_field_definition.fn(client, field)
            try:
                JSON(value=field_definitions).save("mediahaven-field-definitions", overwrite=True)
            except Exception as e:
                logger.error(f"Error saving metadata structure: {e}")
                raise Exception(f"Error saving JSON block: {e}")

        if field_definitions[field]["Family"] not in json_dict["Metadata"]:
            json_dict['Metadata'][field_definitions[field]["Family"]]= {field : value}
        else:
            json_dict['Metadata'][field_definitions[field]["Family"]][field] = value
    return json_dict

@task()
def get_field_definition(client : MediaHaven, field: str) -> dict:
    '''
    Get the field definition from MediaHaven

    Parameters:
        - client: MediaHaven client
        - field: Name of the field

    Returns:
        - field definition
    '''
    logger = get_run_logger()
    field_description = {}
    try:
        field_dict = json.loads(client.fields.get(field=field).raw_response)
        field_description["Family"] = field_dict["Family"]
        field_description["Type"] = field_dict["Type"]
    except Exception as e:
        logger.error(f"Error getting field definition: {field}")
        raise Exception(f"Error getting field definition: {e}")
    return field_description

@task()
def get_client(block_name_prefix: str) -> MediaHaven:
    '''
    Get a MediaHaven client.

    Parameters:
        - block_name_prefix: Prefix of the Block variables that contain the MediaHaven credentials

    Blocks:
        - Secret:
            - {block_name_prefix}-client-secret: Mediahaven API client secret
            - {block_name_prefix}-password: Mediahaven API password
        - String:
            - {block_name_prefix}-client_id: Mediahaven API client ID
            - {block_name_prefix}-username: Mediahaven API username
            - {block_name_prefix}-url: Mediahaven API URL

    Returns:
        - MediaHaven client
    '''
    logger = get_run_logger()
    # Get the credentials
    try:
        url = String.load(f"{block_name_prefix}-url").value
    except ValueError as e:
        logger.error(f"URL not found in block. Please create a String block with name {block_name_prefix}-url")
        raise Exception(f"Error loading URL: {e}")
    try:
        client_id = String.load(f"{block_name_prefix}-client-id").value
    except ValueError as e:
        logger.error(f"Client ID not found in block. Please create a String block with name {block_name_prefix}-client-id")
        raise Exception(f"Error loading client ID: {e}")
    try:
        username = String.load(f"{block_name_prefix}-username").value
    except ValueError as e:
        logger.error(f"Username not found in block. Please create a String block with name {block_name_prefix}-username")
        raise Exception(f"Error loading username: {e}")
    # Get OAuth2 Client and request token
    try:
        grant = ROPCGrant(url, client_id, Secret.load(f"{block_name_prefix}-client-secret").get())
    except ValueError as e:
        logger.error(f"Client secret not found in block. Please create a Secret block with name {block_name_prefix}-client-secret")
        raise Exception(f"Error loading client secret: {e}")
    try:
        grant.request_token(username, Secret.load(f"{block_name_prefix}-password").get())
    except ValueError as e:
        logger.error(f"Password not found in block. Please create a Secret block with name {block_name_prefix}-password")
        raise Exception(f"Error loading password: {e}")
    except RequestTokenError as e:
        logger.error(f"Error requesting token: {e}")
        raise Exception(f"Error requesting token: {e}")
    # Create MediaHaven client
    client = MediaHaven(url, grant)
    return client


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
    '''
    Flow to update metadata in MediaHaven.

    Parameters:
        - fragment_id: ID of the record to update
        - field: Name of the field to update
        - value: Value of the field to update

    Blocks:
        - Secret:
            - {block_name_prefix}-client-secret: Mediahaven API client secret
            - {block_name_prefix}-password: Mediahaven API password
        - String:
            - {block_name_prefix}-client_id: Mediahaven API client ID
            - {block_name_prefix}-username: Mediahaven API username
            - {block_name_prefix}-url: Mediahaven API URL

    '''
    # Create MediaHaven client
    client = get_client.fn("mediahaven-prd")
    # Update metadata
    resp = single_value_metadata_update(client, fragment_id, field, value)

    


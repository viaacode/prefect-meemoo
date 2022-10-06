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
def update_record(client: MediaHaven, fragment_id, xml=None, json=None) -> bool:
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
def get_field_definition(client : MediaHaven, field: str) -> dict:
    '''
    Get the field definition from MediaHaven

    Parameters:
        - client: MediaHaven client
        - field: Name of the field

    Returns:
        - field definition containing the following keys:
            - Family
            - Type
            - Parent (Optional)
    '''
    logger = get_run_logger()
    try:
        field_definition = json.loads(client.fields.get(field=field).raw_response)
    except Exception as e:
        logger.error(f"Error getting field definition: {field}")
        raise Exception(f"Error getting field definition: {e}")
    return field_definition

@task()
def generate_mediahaven_json(client : MediaHaven, field : str, value, merge_strategy : str = None) -> dict:
    '''
    Generate a json object that can be used to update metadata in MediaHaven

    Parameters:
        - client: MediaHaven client
        - field: Name of the field to update
        - value: Value to update the field with
        - merge_strategy: Merge strategy to use when updating the field : KEEP, OVERWRITE, MERGE or SUBTRACT (default: None)
            see: https://mediahaven.atlassian.net/wiki/spaces/CS/pages/722567181/Metadata+Strategy

    Returns:
        - json object  
    '''

    def check_valid_merge_strategy(merge_strategy):
        if merge_strategy not in ["KEEP", "OVERWRITE", "MERGE", "SUBTRACT"]:
            logger.error(f"Invalid merge strategy: {merge_strategy}. Allowed values are KEEP, OVERWRITE, MERGE, SUBTRACT")
            raise ValueError(f"Invalid merge strategy: {merge_strategy}. Allowed values are KEEP, OVERWRITE, MERGE, SUBTRACT")

    def get_field_definitions_block(field):
        # Get the field definitions block
        try:
            field_definitions = JSON.load("mediahaven-field-definitions").value
        except ValueError as e:
            field_definitions = {}
        # Get and Transform the field definition to a dict containing Family, Type and Parent
        if field not in field_definitions:
            field_definition = get_field_definition.fn(client, field)
            field_definitions[field]["Family"] = field_definition["Family"]
            field_definitions[field]["Type"] = field_definition["Type"]
            # Check if the field has a parent
            if field_definition["Parent"]:
                parent_field_definition = get_field_definition.fn(client, field_definition["Parent"])
                field_definition["Parent"] = parent_field_definition["FlatKey"]
                # Save the parent field definition if it's not already in the field definitions
                if field_definitions[field]["Parent"] not in field_definitions:
                    field_definitions[parent_field_definition["FlatKey"]]["Family"] = parent_field_definition["Family"]
                    field_definitions[parent_field_definition["FlatKey"]]["Type"] = parent_field_definition["Type"]
                    if parent_field_definition["Parent"]:
                        logger.error(f"ComplexFields containing ComplexFields not supported: {field}")
                        raise ValueError(f"ComplexFields containing ComplexFields not supported: {field}")
            # Save the field definitions in JSON block
            try:
                JSON(value=field_definitions).save("mediahaven-field-definitions", overwrite=True)
            except Exception as e:
                logger.error(f"Error saving metadata structure: {e}")
                raise e
        return field_definitions

    logger = get_run_logger()
    # Generate the JSON
    json_dict = {'Metadata': {}}
    # Get the field definitions
    field_definitions = get_field_definitions_block(field)
    field_definition = field_definitions[field]
    # Add field and value to generated JSON
    if "Parent" not in field_definition:
        # SimpleFields without a parent field
        if field_definition["Type"] == "SimpleField":
            json_dict['Metadata'][field_definition["Family"]]= {field : value}
        # ComplexFields without a parent field
        else : 
            logger.error("ComplexFields without a parent field are not yet supported")
            raise Exception("ComplexFields without a parent field are not yet supported")
    # Check type of parent
    elif field_definitions[field_definition["Parent"]]["Type"] == "MultiItemField":
        # SimpleFields with a parent field like MultiItemField
        if field_definition["Type"] == "SimpleField":
            json_dict['Metadata'][field_definition["Family"]]= {field_definition["Parent"] : {field : [value]}}
        if merge_strategy:
            check_valid_merge_strategy(merge_strategy)
            json_dict['Metadata']['MergeStrategies'][field] = merge_strategy
    else: 
        logger.error("Only ComplexFields of type MultiItemField are supported for now")
        raise Exception("Only ComplexFields of type MultiItemField are supported for now")

    return json_dict

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
def fragment_metadata_update(client : MediaHaven, fragment_id : str, field_value_dict : dict,) -> bool:
    '''
    Update a single value in MediaHaven

    Parameters:
        - client: MediaHaven client
        - fragment_id: MediaHaven fragment id
        - field_value_dict: Dictionary with FieldDefinition FlatKeys and values

    Returns:
        - True if the update was successful, False otherwise
    '''
    # Get Prefect logger
    logger = get_run_logger()
    # Get JSON format for MediaHaven metadata update
    json_dict = generate_mediahaven_json.fn(client, field_value_dict)
    # Update metadata
    resp = update_record.fn(client, fragment_id, json=json_dict)
    return resp

'''
--- Flows ---
'''

@flow(name="mediahaven-update-single-record-flow")
def main_flow(fragment_id: str, field_flat_key: str, value, ):
    '''
    Flow to update metadata in MediaHaven.

    Parameters:
        - fragment_id: ID of the record to update
        - field: FlatKey of the field to update
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
    resp = fragment_metadata_update(client, fragment_id, {field_flat_key : value})

    


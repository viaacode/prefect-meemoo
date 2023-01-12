import json
import time

from prefect import task, flow, get_run_logger
from prefect.blocks.system import JSON

from mediahaven import MediaHaven
from mediahaven.mediahaven import MediaHavenException
from mediahaven.oauth2 import RequestTokenError

from mergedeep import merge

from prefect_meemoo.credentials import MediahavenCredentials

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
def generate_record_json(client : MediaHaven, field : str, value, merge_strategy : str = None) -> dict:
    '''
    Generate a json object that can be used to update metadata in MediaHaven

    Parameters:
        - client: MediaHaven client
        - field: Name of the field to update
        - value: Value to update the field with
        - merge_strategy: Merge strategy to use when updating the field : KEEP, OVERWRITE, MERGE or SUBTRACT (default: None)
            see: [](https://mediahaven.atlassian.net/wiki/spaces/CS/pages/722567181/Metadata+Strategy)

    Returns:
        - json object  
    '''
    SIMPLE_FIELDS = ["SimpleField", "DateField", "EnumField", "BooleanField", "LongField", "TimeCodeField", "EDTFField"]

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
            field_definitions[field] = {}
            field_definitions[field]["Family"] = field_definition["Family"]
            field_definitions[field]["Type"] = field_definition["Type"]
            # Check if the field has a parent
            if field_definition["ParentId"]:
                parent_field_definition = get_field_definition.fn(client, field_definition["ParentId"])
                field_definitions[field]["Parent"] = parent_field_definition["FlatKey"]
                logger.info(f"Found parent field: {field_definitions[field]['Parent']}")
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
        if field_definition["Type"] in SIMPLE_FIELDS:
            json_dict['Metadata'][field_definition["Family"]]= {field : value}
        # ComplexFields without a parent field
        else : 
            logger.error(f"ComplexFields without a parent field are not yet supported: {field}")
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
        logger.error(f"Only ComplexFields of type MultiItemField are supported for now: {field}")
        raise Exception("Only ComplexFields of type MultiItemField are supported for now")

    return json_dict

@task()
def fragment_metadata_update(client : MediaHaven, fragment_id : str, fields : dict,) -> bool:
    '''
    Generate JSON for updating metadata of a fragment and update in MediaHaven.

    Parameters:
        - client: MediaHaven client
        - fragment_id: MediaHaven fragment id
        - fields: Dictionary with fields and values and optional merge strategies
            ex: {"dcterms_created": {"value": "2022-01-01", "merge_strategy": "KEEP"}}

    Returns:
        - True if the update was successful, False otherwise
    '''
    # Get Prefect logger
    logger = get_run_logger()
    # Get JSON format for MediaHaven metadata update
    json_dict = {}
    for field, content in fields.items():
        merge(json_dict, generate_record_json.fn(client, field, content["value"], content["merge_strategy"]))
    # Update metadata
    resp = update_record.fn(client, fragment_id, json=json_dict)
    return resp

'''
--- Flows ---
'''

@flow(name="mediahaven-update-single-record-flow")
def update_single_value_flow(fragment_id: str, field_flat_key: str, value, ):
    '''
    Flow to update metadata in MediaHaven.

    Parameters:
        - fragment_id: ID of the record to update
        - field: FlatKey of the field to update
        - value: Value of the field to update

    Blocks:
        - MediahavenCredentials:
            - client_secret: Mediahaven API client secret
            - password: Mediahaven API password
            - client_id: Mediahaven API client ID
            - username: Mediahaven API username
            - url: Mediahaven API URL

    '''
    # Get Prefect logger
    logger = get_run_logger()
    # Create MediaHaven client
    try:
        client = MediahavenCredentials.load("mediahaven").get_client("mediahaven-prd")
    except ValueError as e: 
        logger.error(f"Error loading block: {e}")
        raise e
    except RequestTokenError as e:
        logger.error(f"Error requesting token: {e}")
        raise e

    # Update metadata
    resp = fragment_metadata_update(client, fragment_id, {field_flat_key : {"value" : value}})

    


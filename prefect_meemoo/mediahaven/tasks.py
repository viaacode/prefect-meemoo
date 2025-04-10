import json
from typing import List

from mediahaven import MediaHaven
from mediahaven.oauth2 import RequestTokenError
from mediahaven.resources.base_resource import MediaHavenPageObject
from mergedeep import merge
from prefect import flow, get_run_logger, task
from prefect.blocks.system import JSON

from prefect_meemoo.mediahaven.credentials import MediahavenCredentials

'''
--- Tasks ---
'''

'''
--- Organisations ---
'''

@task(name="Get organisation")
def get_organisation(client: MediaHaven, organisation_id: str) -> dict:
    '''
    Get an organisation from MediaHaven

    Parameters:
        - client: MediaHaven client
        - organisation_id: ID of the organisation

    Returns:
        - organisation (dict)
            - ID
            - Name
            - LongName
            - ExternalID
            - CustomProperties
            - TenantGroup
    '''
    logger = get_run_logger()
    try:
        organisation = json.loads(client.organisations.get(organisation_id=organisation_id).raw_response())
        return organisation
    except Exception as e:
        logger.error(e)
        raise e

@task(name="Get organisation")
def get_organisation_by_external_id(client: MediaHaven, external_id: str) -> dict:
    '''
    Get an organisation from MediaHaven by ExternalId

    Parameters:
        - client: MediaHaven client
        - external_id: ExternalId of the organisation

    Returns:
        - organisation (dict)
            - ID
            - Name
            - LongName
            - ExternalID
            - CustomProperties
            - TenantGroup
    '''
    logger = get_run_logger()
    try:
        organisation = json.loads(client.organisations.get_by_external_id(external_id=external_id).raw_response())
        return organisation
    except Exception as e:
        logger.error(e)
        raise e

@task(name="Search organisations")
def search_organisations(client: MediaHaven, **query_params) -> List[dict]:
    '''
    Get a list of organisations from MediaHaven

    Parameters:
        - client: MediaHaven client

    Returns:
        - List of all organisations in MediaHaven (list of dicts)
            - ID
            - Name
            - LongName
            - ExternalID
            - CustomProperties
            - TenantGroup
    '''
    logger = get_run_logger()
    try:
        organisations = json.loads(client.organisations.search(nrOfResults=1000, **query_params).raw_response)
        return organisations['Results']
    except Exception as e:
        logger.error(e)
        raise e

'''
--- Field definitions ---
'''

@task(name="Get field definition")
def get_field_definition(client : MediaHaven, field_flat_key: str) -> dict:
    '''
    Get the field definition from MediaHaven

    Parameters:
        - client: MediaHaven client
        - field: Name of the field

    Returns:
        - field definition (dict)
            - Family
            - Type
            - Parent (Optional)
    '''
    logger = get_run_logger()
    try:
        field_definition = json.loads(client.fields.get(field=field_flat_key).raw_response)
    except Exception as e:
        logger.error(f"Error getting field definition: {field_flat_key}")
        raise Exception(f"Error getting field definition: {e}")
    return field_definition

'''
--- Records ---
'''

@task(name="Update record")
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
    logger = get_run_logger()
    resp = None
    try:
        resp = client.records.update(record_id=fragment_id, json=json, xml=xml)
        logger.info(f"Updated: {fragment_id}")
        return resp
    except Exception as e:
        logger.error(e)
        logger.error("Not updated: " + fragment_id)
        raise e

@task(name="Search mediahaven records")
def search_records(
    client: MediaHaven, query : str, last_modified_date=None, start_index=0, nr_of_results=100, sort:str=""
) -> MediaHavenPageObject:

    """
    Task to query MediaHaven with a given query.

    Parameters:
        - client (MediaHaven): MediaHaven client
        - query (str): Query to execute
        - last_modified_date (str): Last Updated data to filter on
        - start_index (int): Start index of the query
        - nr_of_results (int): Number of results to return

    Returns:
        - dict: Dictionary containing the results of the query  
    """
    logger = get_run_logger()
    # Adding LastModified to query
    if last_modified_date:
        if "[" in last_modified_date or "]" in last_modified_date:
            query += f" +(LastModifiedDate:{last_modified_date})"
        else:
            query += f' +(LastModifiedDate:[{last_modified_date} TO *])'
    log_record= {
        "query": query,
        "start_index": start_index,
        "nr_of_results": nr_of_results,
        "sort": sort
    }
    try:
        records_page = client.records.search(q=query, nrOfResults=nr_of_results, startIndex=start_index, sort=sort)
    except Exception as error:
        log_record["outcome_status"] = "FAIL"
        log_record["status_message"] = error
        logger.error(log_record)
        raise error
    else:
        logger.info({"TotalNrOfResults" : str(records_page.page_result.TotalNrOfResults)})
        log_record["outcome_status"] = "SUCCESS"
        logger.info(log_record)
        return records_page


@task(name="Generate record json")
def generate_record_json(client : MediaHaven, field_flat_key : str, value, merge_strategy : str = None) -> dict:
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
        if merge_strategy not in ["KEEP", "OVERWRITE", "MERGE", "SUBTRACT", None]:
            logger.error(f"Invalid merge strategy: {merge_strategy}. Allowed values are KEEP, OVERWRITE, MERGE, SUBTRACT")
            raise ValueError(f"Invalid merge strategy: {merge_strategy}. Allowed values are KEEP, OVERWRITE, MERGE, SUBTRACT")

    def get_field_definitions_block(field_flat_key):
        # Get the field definitions block
        try:
            field_definitions = JSON.load("mediahaven-field-definitions").value
        except ValueError as e:
            field_definitions = {}
        # Get and Transform the field definition to a dict containing Family, Type and Parent
        if field_flat_key not in field_definitions:
            field_definition = get_field_definition.fn(client, field_flat_key)
            field_definitions[field_flat_key] = {}
            field_definitions[field_flat_key]["Family"] = field_definition["Family"]
            field_definitions[field_flat_key]["Type"] = field_definition["Type"]
            field_definitions[field_flat_key]["Key"] = field_definition["Key"]
            # Check if the field has a parent
            if field_definition["ParentId"]:
                parent_field_definition = get_field_definition.fn(client, field_definition["ParentId"])
                field_definitions[field_flat_key]["Parent"] = parent_field_definition["FlatKey"]
                # Save the parent field definition if it's not already in the field definitions
                if field_definitions[field_flat_key]["Parent"] not in field_definitions:
                    field_definitions[field_definitions[field_flat_key]["Parent"]] = {}
                    field_definitions[parent_field_definition["FlatKey"]]["Family"] = parent_field_definition["Family"]
                    field_definitions[parent_field_definition["FlatKey"]]["Type"] = parent_field_definition["Type"]
                    field_definitions[parent_field_definition["FlatKey"]]["Key"] = parent_field_definition["Type"]
                    if parent_field_definition["ParentId"]:
                        logger.info(f"Parent of parent field: {parent_field_definition['ParentId']}")
                        logger.error(f"ComplexFields containing ComplexFields not supported: {field_flat_key}")
                        raise ValueError(f"ComplexFields containing ComplexFields not supported: {field_flat_key}")
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
    field_definitions = get_field_definitions_block(field_flat_key)
    field_definition = field_definitions[field_flat_key]
    # Add field and value to generated JSON
    if "Parent" not in field_definition:
        # SimpleFields without a parent field
        if field_definition["Type"] in SIMPLE_FIELDS:
            json_dict['Metadata'][field_definition["Family"]]= {field_flat_key : value}
        # ComplexFields without a parent field
        else : 
            logger.error(f"ComplexFields are not yet supported (only children): {field_flat_key} ")
            raise Exception("ComplexFields are not yet supported (only children)")
    # Check type of parent
    elif field_definitions[field_definition["Parent"]]["Type"] == "MultiItemField":
        # SimpleFields with a parent field like MultiItemField
        if field_definition["Type"] == "SimpleField":
            json_dict['Metadata'][field_definition["Family"]]= {field_definition["Parent"] : {field_definition["Key"] : [value]}}
        if merge_strategy:
            check_valid_merge_strategy(merge_strategy)
            json_dict['Metadata']['MergeStrategies'] = {}
            json_dict['Metadata']['MergeStrategies'][field_definition["Parent"]] = merge_strategy
    else: 
        logger.error(f"Only ComplexFields of type MultiItemField are supported for now: {field_flat_key}")
        raise Exception("Only ComplexFields of type MultiItemField are supported for now")

    return json_dict


@task(name='Update metadata of fragment')
def fragment_metadata_update(client : MediaHaven, fragment_id : str, fields : dict,) -> bool:
    '''
    Generate JSON for updating metadata of a fragment and update in MediaHaven.

    Parameters:
        - client: MediaHaven client
        - fragment_id: MediaHaven fragment id
        - fields: Dictionary with field's flatkey and values and optional merge strategies
            ex: {"dcterms_created": {"value": "2022-01-01", "merge_strategy": "KEEP"}}

    Returns:
        - True if the update was successful, False otherwise
    '''
    # Get Prefect logger
    logger = get_run_logger()
    # Get JSON format for MediaHaven metadata update
    json_dict = {}
    for field_flat_key, content in fields.items():
        merge(json_dict, generate_record_json.fn(client, field_flat_key, content["value"], content["merge_strategy"]))
    logger.info(f"JSON for updating metadata of fragment_id: {fragment_id}: {json_dict}")
    # Update metadata
    resp = update_record.fn(client, fragment_id, json=json_dict)
    return resp

'''
--- Flows ---
'''

@flow(name="new name")
def update_single_value_flow(fragment_id: str, field_flat_key: str, value, ):
    '''
    Flow to update metadata in MediaHaven.

    Parameters:
        - fragment_id: ID of the record to update
        - field_flat_key: FlatKey of the field to update
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

    


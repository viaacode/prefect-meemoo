# Mediahaven
## Tasks
- [get_organisation](#get_organisation)
- [search_organisations](#search_organisations)
- [update_record](#update_record)
- [get_field_definition](#get_field_definition)
- [generate_record_json](#generate_record_json)
- [get_client](#get_client)
- [fragment_metadata_update](#fragment_metadata_update)
### get_organisation
get_organisation('client', 'organisation_id')

    Get an organisation from MediaHaven

    Parameters:
        - client: MediaHaven client
        - organisation_id: ID of the organisation

    Returns:
        - organisation
            - ID
            - Name
            - LongName
            - ExternalID
            - CustomProperties
            - TenantGroup
    
### search_organisations
search_organisations('client',)

    Get a list of organisations from MediaHaven

    Parameters:
        - client: MediaHaven client

    Returns:
        - Generator of organisations
            - ID
            - Name
            - LongName
            - ExternalID
            - CustomProperties
            - TenantGroup
    
### update_record
update_record('client', 'fragment_id', 'xml', 'json')

    Update metadata of a fragment.

    Parameters:
        - client: MediaHaven client
        - fragment_id: ID of the fragment to update
        - xml: XML metadata to update
        - json: JSON metadata to update

    Returns:
        - True if the metadata was updated, False otherwise
    
### get_field_definition
get_field_definition('client', 'field_flat_key')

    Get the field definition from MediaHaven

    Parameters:
        - client: MediaHaven client
        - field: Name of the field

    Returns:
        - field definition containing the following keys:
            - Family
            - Type
            - Parent (Optional)
    
### generate_record_json
generate_record_json('client', 'field_flat_key', 'value', 'merge_strategy')

    Generate a json object that can be used to update metadata in MediaHaven

    Parameters:
        - client: MediaHaven client
        - field: Name of the field to update
        - value: Value to update the field with
        - merge_strategy: Merge strategy to use when updating the field : KEEP, OVERWRITE, MERGE or SUBTRACT (default: None)
            see: [](https://mediahaven.atlassian.net/wiki/spaces/CS/pages/722567181/Metadata+Strategy)

    Returns:
        - json object  
    
### get_client
get_client('block_name_prefix',)

    Get a MediaHaven client.

    Parameters:
        - block_name_prefix: Prefix of the Block variables that contain the MediaHaven credentials

    Blocks:
        - Secret:
            - {block_name_prefix}-client-secret: Mediahaven API client secret
            - {block_name_prefix}-password: Mediahaven API password
        - String:
            - {block_name_prefix}-client-id: Mediahaven API client ID
            - {block_name_prefix}-username: Mediahaven API username
            - {block_name_prefix}-url: Mediahaven API URL

    Returns:
        - MediaHaven client
    
### fragment_metadata_update
fragment_metadata_update('client', 'fragment_id', 'fields')

    Generate JSON for updating metadata of a fragment and update in MediaHaven.

    Parameters:
        - client: MediaHaven client
        - fragment_id: MediaHaven fragment id
        - fields: Dictionary with field's flatkey and values and optional merge strategies
            ex: {"dcterms_created": {"value": "2022-01-01", "merge_strategy": "KEEP"}}

    Returns:
        - True if the update was successful, False otherwise
    

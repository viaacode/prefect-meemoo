# Mediahaven
## Tasks
- [get_client](#get_client)
- [get_organisation](#get_organisation)
- [search_organisations](#search_organisations)
- [get_field_definition](#get_field_definition)
- [update_record](#update_record)
- [search_records](#search_records)
- [generate_record_json](#generate_record_json)
- [fragment_metadata_update](#fragment_metadata_update)
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
    
### get_organisation
get_organisation('client', 'organisation_id')

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
    
### search_organisations
search_organisations('client',)

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
    
### get_field_definition
get_field_definition('client', 'field_flat_key')

    Get the field definition from MediaHaven

    Parameters:
        - client: MediaHaven client
        - field: Name of the field

    Returns:
        - field definition (dict)
            - Family
            - Type
            - Parent (Optional)
    
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
    
### search_records
search_records('client', 'query', 'last_modified_date', 'start_index', 'nr_of_results')

    Task to query MediaHaven with a given query.
    Parameters:
        - client (MediaHaven): MediaHaven client
        - query (str): Query to execute
        - last_modified_date (str): Last Updated data to filter on
        - start_index (int): Start index of the query
        - nr_of_results (int): Number of results to return
    Returns:
        - dict: Dictionary containing the results of the query  
    
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
    
# RDF
## Tasks
- [sparql_gsp_post](#sparql_gsp_post)
- [sparql_gsp_put](#sparql_gsp_put)
- [sparql_gsp_delete](#sparql_gsp_delete)
- [sparql_gsp_get](#sparql_gsp_get)
- [sparql_select](#sparql_select)
- [sparql_update_query](#sparql_update_query)
- [sparql_update_insert](#sparql_update_insert)
- [sparql_update_clear](#sparql_update_clear)
- [compare](#compare)
- [json_to_rdf](#json_to_rdf)
- [sparql_transform](#sparql_transform)
- [combine_ntriples](#combine_ntriples)
- [validate_ntriples](#validate_ntriples)
### sparql_gsp_post
sparql_gsp_post('input_data', 'endpoint', 'graph', 'content_type', 'auth', 'timeout')

    Send a POST request to a SPARQL Graph Store HTTP Protocol endpoint

    Parameters:
        - input_data (str): Serialized RDF data to be POSTed to the endpoint
        - endpoint (str): The URL of the SPARQL Graph Store endpoint
        - graph (str, optional): A URI identifying the named graph to post to.
                If set to None, the `endpoint` parameter is assumed to be using
                [Direct Graph Identification](https://www.w3.org/TR/sparql11-http-rdf-update/#direct-graph-identification).
        - content_type (str, optional): the mimeType of the `input_data`. Defaults to "text/turtle".
        - auth (AuthBase, optional): a `requests` library authentication object

    Returns:
        - True if the POST was successful, False otherwise
    
### sparql_gsp_put
sparql_gsp_put('input_data', 'endpoint', 'graph', 'content_type', 'auth', 'timeout')

    Send a PUT request to a SPARQL Graph Store HTTP Protocol endpoint

    Parameters:
        - input_data (str): Serialized RDF data to be PUT to the endpoint
        - endpoint (str): The URL of the SPARQL Graph Store endpoint
        - graph (str, optional): A URI identifying the named graph to put to.
                If set to None, the `endpoint` parameter is assumed to be using
                [Direct Graph Identification](https://www.w3.org/TR/sparql11-http-rdf-update/#direct-graph-identification).
        - content_type (str, optional): the mimeType of the `input_data`. Defaults to "text/turtle".
        - auth (AuthBase, optional): a `requests` library authentication object

    Returns:
        - True if the PUT was successful, False otherwise
    
### sparql_gsp_delete
sparql_gsp_delete('endpoint', 'graph', 'auth', 'timeout')

    Send a DELETE request to a SPARQL Graph Store HTTP Protocol endpoint

    Parameters:
        - endpoint (str): The URL of the SPARQL Graph Store endpoint
        - graph (str, optional): A URI identifying the named graph to delete.
                If set to None, the `endpoint` parameter is assumed to be using
                [Direct Graph Identification](https://www.w3.org/TR/sparql11-http-rdf-update/#direct-graph-identification).
        - auth (AuthBase, optional): a `requests` library authentication object

    Returns:
        - True if the DELETE was successful, False otherwise
    
### sparql_gsp_get
sparql_gsp_get('endpoint', 'graph', 'content_type', 'auth', 'timeout')

    Send a GET request to a SPARQL Graph Store HTTP Protocol endpoint

    Parameters:
        - endpoint (str): The URL of the SPARQL Graph Store endpoint
        - graph (str, optional): A URI identifying the named graph to get.
                If set to None, the `endpoint` parameter is assumed to be using
                [Direct Graph Identification](https://www.w3.org/TR/sparql11-http-rdf-update/#direct-graph-identification).
        - content_type (str, optional): the deisred mimeType of the result. Defaults to "text/turtle".
        - auth (AuthBase, optional): a `requests` library authentication object

    Returns:
        - True if the POST was successful, False otherwise
    
### sparql_select
sparql_select('query', 'endpoint', 'method', 'headers', 'auth')

    Execute SPARQL SELECT query on a SPARQL endpoint and get the results in a pandas dataframe.

    Parameters:
        - query (str): SPARQL SELECT query to execute
        - endpoint (str): The URL of the SPARQL endpoint
        - method (str): The HTTP method to use. Defaults to POST
        - headers (dict, optional): Python dict with HTTP headers to add.
        - auth (AuthBase, optional): a `requests` library authentication object

    Returns:
        - Pandas DataFrame with query results
    
### sparql_update_query
sparql_update_query('query', 'endpoint', 'method', 'headers', 'auth')

    Execute SPARQL Update on a SPARQL endpoint.

    Parameters:
        - query (str): SPARQL Update query to execute
        - endpoint (str): The URL of the SPARQL endpoint
        - method (str): The HTTP method to use. Defaults to POST
        - headers (dict, optional): Python dict with HTTP headers to add.
        - auth (AuthBase, optional): a `requests` library authentication object

    Returns:
        - True if the request was successful, False otherwise
    
### sparql_update_insert
sparql_update_insert('triples', 'endpoint', 'graph')

    Insert an iterable of RDFLib triples using SPARQL Update.

    Parameters:
        - triples (List): List of triples
        - endpoint (str): The URL of the SPARQL endpoint
        - graph (str, optional): A URI identifying the named graph to insert the triples into. If set to `None`, the default graph is assumed.

    Returns:
        - True if the request was successful, False otherwise
    
### sparql_update_clear
sparql_update_clear('graph', 'endpoint', 'silent')

    Clear a graph using SPARQL Update.

    Parameters:
        - graph (str): A URI identifying the named graph to insert the triples into.
        - endpoint (str): The URL of the SPARQL endpoint
        - silent (bool):

    Returns:
        - True if the request was successful, False otherwise
    
### compare
compare('input_data1', 'input_data2')
None
### json_to_rdf
json_to_rdf()

    Converts JSON documents to RDF by direct mapping

    Args:
        input_data*: arbitrary list of JSON strings to map
        ns (str, optional): Namespace to use to build RDF predicates. Defaults to https://data.hetarchief.be/ns/source#.

    Returns:
        str: ntriples serialization of the result
    
### sparql_transform
sparql_transform('input_data', 'query')

    Transforms one RDF graph in another using a CONSTRUCT query

    Args:
        *input_data: input RDF graph serialized as ntriples.
        query (str): SPARQL construct query either as file path or as query text.

    Returns:
        str: result RDF graph serialized as ntriples
    
### combine_ntriples
combine_ntriples()

    Concatenates a couple of ntriples lines

    Returns:
        str*: ntriple line to add
    
### validate_ntriples
validate_ntriples('input_data', 'shacl_graph', 'ont_graph')
None
# RDF Parse
## Tasks

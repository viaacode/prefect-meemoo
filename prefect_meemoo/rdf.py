import os.path
from io import StringIO
from typing import Any, Dict, Optional

import pandas as pd
import requests
from prefect import get_run_logger, task
from pyshacl import validate
from rdflib import Graph, Namespace
from requests.auth import AuthBase, HTTPBasicAuth, HTTPDigestAuth
from SPARQLWrapper import CSV, DIGEST, GET, POST, POSTDIRECTLY, SPARQLWrapper
from SPARQLWrapper.Wrapper import BASIC

from prefect_meemoo.rdf_parse import parse_json

METHODS = {"GET": GET, "POST": POST}
SRC_NS = "https://data.hetarchief.be/ns/source#"
TIMEOUT = 0.500

"""
--- Tasks wrt RDF ---
"""

# SPARQL 1.1 Graph Store HTTP Protocol
@task(name="SPARQL Graph Store 1.1 POST")
def sparql_gsp_post(
    input_data: str,
    endpoint: str,
    graph: str = None,
    content_type: str = "text/turtle",
    auth: AuthBase = None,
    timeout: float = TIMEOUT,
):
    """
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
    """
    graph_endpoint = f"{endpoint}?graph={graph}" if graph is not None else endpoint
    req = requests.post(
        url=graph_endpoint,
        headers={"Content-Type": content_type},
        timeout=timeout,
        auth=auth,
        data=input_data,
    )
    if req.status_code >= 400:
        raise Exception(f"POST request to {graph_endpoint} failed: {req.status_code}")
    return True


@task(name="SPARQL Graph Store 1.1 PUT")
def sparql_gsp_put(
    input_data: str,
    endpoint: str,
    graph: str = None,
    content_type: str = "text/turtle",
    auth: AuthBase = None,
    timeout: float = TIMEOUT,
):
    """
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
    """
    graph_endpoint = f"{endpoint}?graph={graph}" if graph is not None else endpoint
    req = requests.put(
        url=graph_endpoint,
        headers={"Content-Type": content_type},
        timeout=timeout,
        auth=auth,
        data=input_data,
    )
    if req.status_code >= 400:
        raise Exception(f"PUT request to {graph_endpoint} failed: {req.status_code}")
    return True


@task(name="SPARQL Graph Store 1.1 DELETE")
def sparql_gsp_delete(
    endpoint: str, graph: str = None, auth: AuthBase = None, timeout: float = TIMEOUT
):
    """
    Send a DELETE request to a SPARQL Graph Store HTTP Protocol endpoint

    Parameters:
        - endpoint (str): The URL of the SPARQL Graph Store endpoint
        - graph (str, optional): A URI identifying the named graph to delete.
                If set to None, the `endpoint` parameter is assumed to be using
                [Direct Graph Identification](https://www.w3.org/TR/sparql11-http-rdf-update/#direct-graph-identification).
        - auth (AuthBase, optional): a `requests` library authentication object

    Returns:
        - True if the DELETE was successful, False otherwise
    """
    graph_endpoint = f"{endpoint}?graph={graph}" if graph is not None else endpoint
    req = requests.delete(
        url=graph_endpoint,
        auth=auth,
        timeout=timeout,
    )
    if req.status_code >= 400:
        raise Exception(f"Delete of {graph_endpoint} failed: {req.status_code}")
    return True


# SPARQL 1.1 Graph Store HTTP Protocol
@task(name="SPARQL Graph Store 1.1 GET")
def sparql_gsp_get(
    endpoint: str,
    graph: str = None,
    content_type: str = "text/turtle",
    auth: AuthBase = None,
    timeout: float = TIMEOUT,
):
    """
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
    """
    graph_endpoint = f"{endpoint}?graph={graph}" if graph is not None else endpoint
    req = requests.get(
        url=graph_endpoint,
        headers={"Accept": content_type},
        auth=auth,
        timeout=timeout,
    )
    if req.status_code >= 400:
        raise Exception(f"POST request to {graph_endpoint} failed: {req.status_code}")
    return req.text


@task(name="execute SPARQL SELECT query")
def sparql_select(
    query: str,
    endpoint: str,
    method: str = "POST",
    headers: Optional[Dict[str, Any]] = None,
    auth: AuthBase = None,
):
    """
    Execute SPARQL SELECT query on a SPARQL endpoint and get the results in a pandas dataframe.

    Parameters:
        - query (str): SPARQL SELECT query to execute
        - endpoint (str): The URL of the SPARQL endpoint
        - method (str): The HTTP method to use. Defaults to POST
        - headers (dict, optional): Python dict with HTTP headers to add.
        - auth (AuthBase, optional): a `requests` library authentication object

    Returns:
        - Pandas DataFrame with query results
    """
    logger = get_run_logger()
    sparql = create_sparqlwrapper(endpoint, method, auth)
    query = resolve_query(query)
    sparql.setQuery(query)

    if not sparql.isSparqlQueryRequest():
        logger.warning("Query is an update query.")

    if sparql.method == POST:
        sparql.setOnlyConneg(True)
        sparql.addCustomHttpHeader("Content-type", "application/sparql-query")
        sparql.addCustomHttpHeader("Accept", "text/csv")
        sparql.setRequestMethod(POSTDIRECTLY)

    if headers is not None:
        for h in headers.items():
            sparql.addCustomHttpHeader(h[0], h[1])

    logger.info("Sending query to %.", endpoint)

    sparql.setReturnFormat(CSV)
    results = sparql.query().convert()
    _csv = StringIO(results.decode("utf-8"))
    return pd.read_csv(_csv, sep=",")


# SPARQL 1.1 Update
@task(name="execute SPARQL Update query")
def sparql_update_query(
    query: str,
    endpoint: str,
    method: str = "POST",
    headers: Optional[Dict[str, Any]] = None,
    auth: AuthBase = None,
):
    """
    Execute SPARQL Update on a SPARQL endpoint.

    Parameters:
        - query (str): SPARQL Update query to execute
        - endpoint (str): The URL of the SPARQL endpoint
        - method (str): The HTTP method to use. Defaults to POST
        - headers (dict, optional): Python dict with HTTP headers to add.
        - auth (AuthBase, optional): a `requests` library authentication object

    Returns:
        - True if the request was successful, False otherwise
    """
    logger = get_run_logger()
    sparql = create_sparqlwrapper(endpoint, method, auth)
    query = resolve_query(query)
    sparql.setQuery(query)

    if sparql.isSparqlUpdateRequest():
        logger.warning("Query is not an update query.")

    if headers is not None:
        for h in headers.items():
            sparql.addCustomHttpHeader(h[0], h[1])

    logger.info("Sending query to %.", endpoint)

    results = sparql.query()
    logger.info(results.response.read())

    sparql.resetQuery()


@task(name="insert RDF triples")
def sparql_update_insert(triples, endpoint, graph=None):
    """
    Insert an iterable of RDFLib triples using SPARQL Update.

    Parameters:
        - triples (List): List of triples
        - endpoint (str): The URL of the SPARQL endpoint
        - graph (str, optional): A URI identifying the named graph to insert the triples into. If set to `None`, the default graph is assumed.

    Returns:
        - True if the request was successful, False otherwise
    """

    query = "INSERT DATA {\n"

    if graph is not None:
        query += f"GRAPH <{graph}> {{\n"

    for t in triples:
        query += to_ntriples(t)

    query += "}\n"

    if graph is not None:
        query += "}"

    return sparql_update_query(query, endpoint)


@task(name="convert json to rdf")
def json_to_rdf(*input_data: str, ns: str = SRC_NS):
    """
    Converts JSON documents to RDF by direct mapping

    Args:
        input_data*: arbitrary list of JSON strings to map
        ns (str, optional): Namespace to use to build RDF predicates. Defaults to https://data.hetarchief.be/ns/source#.

    Returns:
        str: ntriples serialization of the result
    """
    g = Graph(store="Oxigraph")
    for data in input_data:
        if data is None:
            continue

        for t in parse_json(data, namespace=Namespace(ns)):
            g.add(t)
    return g.serialize(format="nt")


@task(name="sparql transformation")
def sparql_transform(input_data: str, query: str):
    """
    Transforms one RDF graph in another using a CONSTRUCT query

    Args:
        *input_data: input RDF graph serialized as ntriples.
        query (str): SPARQL construct query either as file path or as query text.

    Returns:
        str: result RDF graph serialized as ntriples
    """

    input_graph = Graph(store="Oxigraph")
    output_graph = Graph(store="Oxigraph")

    query = resolve_query(query)

    input_graph.parse(data=input_data, format="nt")

    results = input_graph.query(query)

    for result in results:
        output_graph.add(result)

    return output_graph.serialize(format="nt")


@task(name="concatenate ntriples")
def combine_ntriples(*ntriples: str):
    """
    Concatenates a couple of ntriples lines

    Returns:
        str*: ntriple line to add
    """
    temp = "\n".join(ntriples)
    return temp


@task(name="validate ntriples")
def validate_ntriples(input_data: str, shacl_graph: str, ont_graph: str = None):

    logger = get_run_logger()
    input_graph = Graph()
    input_graph.parse(data=input_data)

    r = validate(
        input_graph,
        shacl_graph=shacl_graph,
        # ont_graph=ont_graph,
        allow_infos=True,
        allow_warnings=True,
    )

    conforms, results_graph, results_text = r
    logger.info(results_text)
    return conforms


def to_ntriples(t, namespace_manager=None):
    return (
        f"{t[0].n3(namespace_manager)} "
        f"{t[1].n3(namespace_manager)} "
        f"{t[2].n3(namespace_manager)} . \n"
    )


def create_sparqlwrapper(endpoint: str, method: str = None, auth: AuthBase = None):
    sparql = SPARQLWrapper(endpoint)

    if auth is not None:
        if isinstance(auth, HTTPBasicAuth):
            sparql.setHTTPAuth(BASIC)
            sparql.setCredentials(auth.username, auth.password)
        elif isinstance(auth, HTTPDigestAuth):
            sparql.setHTTPAuth(DIGEST)
            sparql.setCredentials(auth.username, auth.password)
        else:
            raise NotImplementedError()

    sparql.setMethod(METHODS[method])

    return sparql


def resolve_query(query):
    logger = get_run_logger()
    query_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), query)
    if os.path.isfile(query_path):
        with open(query_path, encoding="utf-8") as f:
            query = f.read()
    else:
        logger.warning("Query does not point to a file; executing as query text.")
    return query

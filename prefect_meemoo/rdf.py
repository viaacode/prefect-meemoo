import os.path
from typing import Any, Dict, Optional

import requests
from prefect import get_run_logger, task
from rdf_parse import parse_json
from rdflib import Graph, Namespace
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from SPARQLWrapper import DIGEST, GET, POST, SPARQLWrapper
from SPARQLWrapper.Wrapper import BASIC

AUTH_TYPES = {HTTPBasicAuth: BASIC, HTTPDigestAuth: DIGEST}
METHODS = {"GET": GET, "POST": POST}
SRC_NS = "https://data.hetarchief.be/ns/source#"

"""
--- Tasks wrt RDF ---
"""

# SPARQL 1.1 Graph Store HTTP Protocol
def sparql_gsp_post(
    input_data: str,
    endpoint: str,
    graph: str = None,
    contentType: str = "text/turtle",
    auth=None,
):
    """
    Send POST request to a SPARQL Graph Store Protocol endpoint

    :param input_data: str
    """
    graph_endpoint = f"{endpoint}?graph={graph}" if graph is not None else endpoint
    r_post = requests.request(
        "POST",
        url=graph_endpoint,
        headers={"Content-Type": contentType},
        auth=auth,
        data=input_data,
    )
    return r_post.status_code < 400


# SPARQL 1.1 Update


@task(name="execute SPARQL Update query")
def sparql_update(
    query: str,
    endpoint: str,
    method: str = "GET",
    headers: Optional[Dict[str, Any]] = None,
    auth_type: Any = HTTPBasicAuth,
    login: str = None,
    password: str = None,
):
    """
    Execute SPARQL Update on a SPARQL endpoint.

    """
    logger = get_run_logger()
    sparql = SPARQLWrapper(endpoint)

    if auth_type in AUTH_TYPES:
        sparql.setHTTPAuth(AUTH_TYPES[auth_type])

    sparql.setCredentials(login, password)
    sparql.setMethod(METHODS[method])

    query_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), query)
    if os.path.isfile(query_path):
        with open(query_path, encoding="utf-8") as f:
            query = f.read()
    else:
        logger.warning("Query does not point to a file; executing as query text.")

    sparql.setQuery(query)

    if not sparql.isSparqlUpdateRequest():
        logger.warning("Query is not an update query.")

    if headers is not None:
        for h in headers.items():
            sparql.addCustomHttpHeader(h[0], h[1])

    logger.info(f"Sending query to {endpoint}")

    results = sparql.query()
    logger.info(results.response.read())

    sparql.resetQuery()


@task(name="insert RDF triples")
def insert(triples, endpoint, graph=None):
    query = "INSERT DATA {\n"

    if graph is not None:
        query += f"GRAPH <{graph}> {{\n"

    for t in triples:
        query += to_ntriples(t)

    query += "}\n"

    if graph is not None:
        query += "}"

    sparql_update(query, endpoint)


def to_ntriples(t, namespace_manager=None):
    return (
        f"{t[0].n3(namespace_manager)} "
        f"{t[1].n3(namespace_manager)} "
        f"{t[2].n3(namespace_manager)} . \n"
    )


@task(name="convert json to rdf")
def json_to_rdf(input_data, ns=SRC_NS):
    g = Graph(store="Oxigraph")
    for t in parse_json(input_data, namespace=Namespace(ns)):
        g.add(t)
    return g.serialize(format="nt")


@task(name="sparql transformation")
def sparql_transform(input_data, query):
    logger = get_run_logger()
    input_graph = Graph(store="Oxigraph")
    output_graph = Graph(store="Oxigraph")

    query_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), query)
    if os.path.isfile(query_path):
        with open(query_path, encoding="utf-8") as f:
            query = f.read()
    else:
        logger.warning("Query does not point to a file; executing as query text.")

    input_graph.parse(data=input_data, format="nt")

    results = input_graph.query(query)

    for result in results:
        output_graph.add(result)

    return output_graph.serialize(format="nt")


@task(name="concatenate ntuples")
def combine_ntuples(*ntuples):
    temp = "\n".join(ntuples)
    return temp

import os.path
from collections import deque
from typing import Any, Optional, Dict

import ijson
from prefect import get_run_logger, task
from pyoxigraph import *
from rdflib import BNode, Graph, Literal, Namespace
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from SPARQLWrapper import DIGEST, GET, POST, SPARQLWrapper
from SPARQLWrapper.Wrapper import BASIC

AUTH_TYPES = {HTTPBasicAuth: BASIC, HTTPDigestAuth: DIGEST}
METHODS = {"GET": GET, "POST": POST}
SRC_NS = "https://data.hetarchief.be/ns/source#"

"""
--- Tasks wrt RDF ---
"""


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
        with open(query_path) as f:
            query = f.read()
    else:
        logger.warning("Query does not point to a file; executing as query text.")

    sparql.setQuery(query)

    if not sparql.isSparqlUpdateRequest():
        logger.warning("Query is not an update query.")

    if headers is not None:
        for h in headers.items():
            sparql.addCustomHttpHeader(h[0], h[1])

    logger.info("Sending query to {}".format(endpoint))

    results = sparql.query()
    logger.info(results.response.read())

    sparql.resetQuery()


@task(name="insert RDF triples")
def insert(triples, graph=None):
    query = "INSERT DATA {\n"

    if graph is not None:
        query += "GRAPH <{}> {{\n".format(graph)

    for t in triples:
        query += to_ntriples(t)

    query += "}\n"

    if graph is not None:
        query += "}"

    sparql_update(query)


def to_ntriples(t, namespace_manager=None):
    return "{} {} {} . \n".format(
        t[0].n3(namespace_manager),
        t[1].n3(namespace_manager),
        t[2].n3(namespace_manager),
    )


@task(name="convert json to rdf")
def json_to_rdf(input_data, ns=SRC_NS):
    g = Graph(store="Oxigraph")
    for t in parse_json(input_data, namespace=Namespace(ns)):
        g.add(t)
    return g.serialize(format="nt")


@task(name="sparql transformation")
def sparql_transform(input_data, query_location):
    temp_input_graph = Graph(store="Oxigraph")
    temp_output_graph = Graph(store="Oxigraph")

    query_file = open(query_location, "r")
    query = query_file.read()
    query_file.close()

    temp_input_graph.parse(data=input_data, format="nt")

    results = temp_input_graph.query(query)

    for result in results:
        temp_output_graph.add(result)

    return temp_output_graph.serialize(format="nt")


@task(name="concatenate ntuples")
def combine_ntuples(*ntuples):
    temp = "\n".join(ntuples)
    return temp


def parse_dict(data, **kwargs):
    """Generates RDFlib triples from a python dictionary using a direct mapping."""

    def basic_parse(data):
        if isinstance(data, dict):  # start_map
            yield "start_map", None
            for k, v in data.items():
                yield "map_key", k
                for event, value in basic_parse(v):
                    yield event, value
            yield "end_map", None
        elif isinstance(data, list):  # start_list
            yield "start_array", None
            for i in data:
                for event, value in basic_parse(i):
                    yield event, value
            yield "end_array", None
        elif data is None:
            yield "null", data
        elif isinstance(data, str):
            yield "string", data
        elif isinstance(data, bool):
            yield "boolean", data
        elif isinstance(data, int):
            yield "integer", data
        elif isinstance(data, float):
            yield "double", data

    events = basic_parse(data)
    return _parse_events(events, **kwargs)


def parse_json(json, **kwargs):
    """
    Generates RDFlib triples from a file-like object
    or a string using a direct mapping.
    """

    #   parse json
    events = ijson.basic_parse(json, use_float=True)

    return _parse_events(events, **kwargs)


def _parse_events(events, **kwargs):
    """
    Internal method that generates RDFlib triples
    from a generator function that yields event, value pairs.
    """

    # initalize defaults
    namespace = Namespace("http://localhost/")
    instance_ns = None

    if "namespace" in kwargs and isinstance(kwargs["namespace"], Namespace):
        namespace = kwargs["namespace"]

    if "instance_ns" in kwargs and isinstance(kwargs["instance_ns"], Namespace):
        instance_ns = kwargs["instance_ns"]

    # initializing deque
    subjectStack = deque([])
    arrayProperties = {}
    prop = None

    i = 0
    for event, value in events:
        if event == "start_array" and subjectStack and prop is not None:
            # fetching the last subject
            s = subjectStack[-1]
            arrayProperties[s] = prop

        if event == "end_array" and subjectStack:
            # fetching the last subject
            s = subjectStack[-1]
            arrayProperties.pop(s, None)

        if event == "start_map":
            if instance_ns is not None:
                subject = instance_ns[str(i)]
                i += 1
            else:
                subject = BNode()
            # add triple with current array property, if any
            if prop is not None and subjectStack:
                # fetching the last subject
                s = subjectStack[-1]
                yield (s, prop, subject)
            subjectStack.append(subject)

        if event == "end_map":
            subjectStack.pop()

            # restore previous array property, if there was any
            if subjectStack and subjectStack[-1] in arrayProperties:
                prop = arrayProperties[subjectStack[-1]]

        if event in ["boolean", "integer", "double", "number"]:
            yield (subjectStack[-1], prop, Literal(value))

        if event == "string" and prop is not None:
            yield (subjectStack[-1], prop, Literal(value))
            # yield (subjectStack[-1], property, Literal(value, datatype=XSD.string))

        if event == "map_key":
            prop = namespace[value]

import pytest
from prefect import flow
from prefect.blocks.core import Block
from rdflib import Graph
from rdflib.compare import to_isomorphic

from prefect_meemoo.triply import run_triplyetl


def rdf_is_equal(expected, actual):
    g_expected = Graph().parse(data=expected)
    g_actual = Graph().parse(file=actual)
    return to_isomorphic(g_expected) == to_isomorphic(g_actual)


def test_run_triplyetl():
    @flow(name="prefect_flow_triplyetl")
    def test_flow():
        run_triplyetl(etl_script_path="./tests/etl/dist/index.js")

    result = test_flow()

    expected = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

    <https://data.hetarchief.be/id/OR-xxxxx> a <https://schema.org/Person>;
    <https://schema.org/name> "xx".
    """

    assert result
    assert rdf_is_equal(expected, "./etl/static/output.ttl")


def test_add_block_as_variables():
    @flow(name="prefect_flow_triplyetl_block")
    def test_flow():
        run_triplyetl(
            etl_script_path="./tests/etl/dist/variables_block.js",
            triply=Block(test="test"),
        )

    result = test_flow()

    expected = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

    <https://data.hetarchief.be/id/Jane> rdfs:label "test-block".
    """

    assert result
    assert rdf_is_equal(expected, "./etl/static/output-block.ttl")


def test_run_triplyetl_with_variables():
    @flow(name="prefect_flow_triplyetl_variables")
    def test_flow():
        run_triplyetl(
            etl_script_path="./tests/etl/dist/variables.js", TEST="test-value"
        )

    result = test_flow()

    expected = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

    <https://data.hetarchief.be/id/Jane> rdfs:label "test-value".
    """

    assert result
    assert rdf_is_equal(expected, "./etl/static/output-variables.ttl")


def test_run_triplyetl_with_error():
    @flow(name="prefect_flow_triplyetl_error")
    def test_flow():
        run_triplyetl(etl_script_path="./tests/etl/dist/error.js")

    with pytest.raises(Exception):
        test_flow()

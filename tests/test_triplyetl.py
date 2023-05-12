import pytest
from prefect import flow
from prefect.blocks.core import Block
from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff

from prefect_meemoo.triplydb.tasks import run_triplyetl


def rdf_is_equal(expected, actual):
    g_expected = Graph().parse(data=expected)
    g_actual = Graph().parse(actual)

    iso_expected = to_isomorphic(g_expected)
    iso_actual = to_isomorphic(g_actual)

    in_both, in_first, in_second = graph_diff(iso_expected, iso_actual)
    print(
        "-".join(("\n" + in_first.serialize(format="nt").lstrip()).splitlines(True))
        + "+".join(("\n" + in_second.serialize(format="nt").lstrip()).splitlines(True))
    )

    return iso_expected == iso_actual


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
    assert rdf_is_equal(expected, "./tests/etl/output/output.ttl")


def test_add_block_as_variables():
    @flow(name="prefect_flow_triplyetl_block")
    def test_flow():
        run_triplyetl(
            etl_script_path="./tests/etl/dist/variables_block.js",
            triply=Block(test="test-block"),
        )

    result = test_flow()

    expected = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

    <https://data.hetarchief.be/id/Jane> rdfs:label "test-block".
    """

    assert result
    assert rdf_is_equal(expected, "./tests/etl/output/output-block.ttl")


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
    assert rdf_is_equal(expected, "./tests/etl/output/output-variables.ttl")

def test_run_triplyetl_with_none_variable():
    @flow(name="prefect_flow_triplyetl_none_variables")
    def test_flow():
        run_triplyetl(
            etl_script_path="./tests/etl/dist/variables.js", TEST=None
        )

    result = test_flow()

    expected = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

    <https://data.hetarchief.be/id/Jane> rdfs:label "undefined".
    """

    assert result
    assert rdf_is_equal(expected, "./tests/etl/output/output-variables.ttl")

def test_run_triplyetl_with_none_variable_assert():
    @flow(name="prefect_flow_triplyetl_none_variables_assert")
    def test_flow():
        run_triplyetl(
            etl_script_path="./tests/etl/dist/variables_assert.js", TEST=None
        )

    with pytest.raises(Exception):
        test_flow()

def test_run_triplyetl_with_error():
    @flow(name="prefect_flow_triplyetl_error")
    def test_flow():
        run_triplyetl(etl_script_path="./tests/etl/dist/error.js")

    with pytest.raises(Exception):
        test_flow()


def test_run_triplyetl_with_validate():
    @flow(name="prefect_flow_triplyetl_validate")
    def test_flow():
        run_triplyetl(etl_script_path="./tests/etl/dist/validation.js")

    assert test_flow()


def test_run_triplyetl_with_validate_violation():
    @flow(name="prefect_flow_triplyetl_validate_violation")
    def test_flow():
        run_triplyetl(etl_script_path="./tests/etl/dist/validation_violation.js")

    with pytest.raises(Exception):
        test_flow()

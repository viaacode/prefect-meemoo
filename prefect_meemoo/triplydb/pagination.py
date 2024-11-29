import requests
from requests import Response
from urllib.parse import urlencode
from typing import Any, Union, Optional
import typing

from prefect import flow, task, get_run_logger

from .credentials import TriplyDBCredentials

PAGE_SIZE = 10_000


@flow
def run_saved_query(
    saved_query_uri: str,
    triplydb_block_name: str,
) -> list[dict[str, Any]]:
    """
    A Prefect flow that executes a saved query with automatic pagination.
    """

    logger = get_run_logger()
    results = []
    page = 0
    while True:
        params = {"page": page + 1, "pageSize": PAGE_SIZE}
        uri = add_params_to_uri(saved_query_uri, params)
        response = request_triply_get(uri, triplydb_block_name)

        json = response.json()
        logger.info(
            f"Query page {page}, pageSize {PAGE_SIZE} - got {len(json)} results"
        )
        results += json
        page += 1

        if len(json) < PAGE_SIZE:
            break
    return results


@flow
def run_sparql_select(
    endpoint: str,
    sparql_template_list: Union[list[str], str],
    triplydb_block_name: str,
    offset_start: int = 0,
) -> list[dict[str, Any]]:
    """
    Prefect flow that sends the given queries to the endpoint with automatic pagination.

    The queries should contain a "OFFSET 0" marker that is used for pagination.
    """

    logger = get_run_logger()
    sparql_template_list = cast_list(sparql_template_list)
    results = []
    for sparql_template in sparql_template_list:
        logger.info("Start of next query execution")
        if "OFFSET 0" not in sparql_template:
            raise Exception("Missing OFFSET in SPARQL query template")

        offset = offset_start
        while True:
            paginated_query = sparql_template.replace("OFFSET 0", f"OFFSET {offset}")
            response = request_triply_post(
                endpoint, paginated_query, triplydb_block_name
            )

            json = response.json()
            logger.info(
                f"Query with OFFSET {offset}, page size {PAGE_SIZE} - got {len(json)} results"
            )
            results += json
            offset += PAGE_SIZE

            if len(json) < PAGE_SIZE:
                break
    return results


def cast_list(list_or_str: Union[list[str], str]) -> list[str]:
    if type(list_or_str) is str:
        list_or_str = [list_or_str]
    return typing.cast(list[str], list_or_str)


@task
def request_triply_get(
    endpoint: str,
    triplydb_block_name: str,
    extra_headers: Optional[dict[str, str]] = None,
) -> Response:
    """
    Send a GET request including the triply token to the given endpoint.
    """
    logger = get_run_logger()

    # Load credentials
    credentials = TriplyDBCredentials.load(triplydb_block_name)
    bearer_token = credentials.token.get_secret_value()

    # Send GET request
    headers = get_triply_headers(bearer_token, extra_headers)
    logger.info(f"Sending GET request to {endpoint}")
    response = requests.get(endpoint, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Status code {response.status_code} - {response.reason}")
    return response


@task(retries=5, retry_delay_seconds=1)
def request_triply_post(
    endpoint: str,
    body: str,
    triplydb_block_name: str,
    extra_headers: Optional[dict[str, str]] = None,
) -> Response:
    """
    Send a POST request containing the triply token to the given endpoint.
    """
    logger = get_run_logger()

    credentials = TriplyDBCredentials.load(triplydb_block_name)
    bearer_token = credentials.token.get_secret_value()

    extra_headers = {} if extra_headers is None else extra_headers
    content_type = {"Content-Type": "application/sparql-query"}
    headers = get_triply_headers(
        bearer_token, extra_headers=extra_headers | content_type
    )

    logger.info(f"Sending POST request to {endpoint}")
    response = requests.post(endpoint, headers=headers, data=body)

    if response.status_code != 200:
        raise Exception(f"Status code {response.status_code} - {response.reason}")

    return response


def get_triply_headers(
    bearer_token: str, extra_headers: Union[dict[str, str], None] = None
) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {bearer_token}",
    }
    extra_headers = extra_headers if extra_headers else {}
    return headers | extra_headers


def add_params_to_uri(uri: str, params: dict[str, Any]) -> str:
    encoded_params = urlencode(params)
    return f"{uri}?{encoded_params}" if "?" not in uri else f"{uri}&{encoded_params}"

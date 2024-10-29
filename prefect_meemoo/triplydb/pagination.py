import requests
from requests import Response
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Any, Callable, Iterable
from itertools import islice
import re

from prefect import task, get_run_logger

from .credentials import TriplyDBCredentials

PAGE_SIZE = 10_000


def run_saved_query(
    saved_query_uri: str,
    triplydb_block_name: str,
    limit: int = 10_000,
    offset: int = 0,
) -> Iterable:
    """
    Execute a saved query.

    Unlike a simple GET request to a saved query endpoint, this function takes care of pagination. Requires prefect.
    Results are yielded back as an Iterable. This means that only part of the results are kept in memory at any given time.

    ```py
    results = run_saved_query(...)
    for r in results:
        ...
    ```

    One caveat with the `offset` parameter is that all results up to #`offset + limit` are fetched from the triple store,
    including the first #`offset` results which are discarded afterwards.

    Use a negative `limit` to fetch all results.
    """

    logger = get_run_logger()

    def send_request(page: int):
        uri = add_params_to_uri(
            saved_query_uri, {"page": page + 1, "pageSize": PAGE_SIZE}
        )
        logger.warning(uri)
        return request_triply_get(uri, triplydb_block_name)

    results = _run_query(send_request)
    if limit < 0:
        return results

    return islice(results, offset, offset + limit)


def run_sparql(
    endpoint: str,
    sparql: str,
    triplydb_block_name: str,
    limit: int = 10_000,
    offset: int = 0,
) -> Iterable:
    """
    Execute a sparql query using the given endpoint.

    Unlike a simple POST request to a tripple store, this function takes care of pagination. Requires prefect.
    Results are yielded back as an Iterable. This means that only part of the results are kept in memory at any given time.

    ```py
    results = run_sparql(...)
    for r in results:
        ...
    ```

    One caveat with the `offset` parameter is that all results up to #`offset + limit` are fetched from the triple store,
    including the first #`offset` results which are discarded afterwards.

    Use a negative `limit` to fetch all results.
    """
    logger = get_run_logger()

    # Check for `OFFSET` clause
    match = re.search(r"(?<!\w)offset\s*", sparql, flags=re.MULTILINE + re.IGNORECASE)
    if match is not None:
        raise Exception(
            "The SPARQL query given to run_sparql must not contain an OFFSET clause"
        )

    # Check for `LIMIT` clause
    match = re.search(rf"(?<!\w)limit\s*", sparql, flags=re.MULTILINE + re.IGNORECASE)
    if match is not None:
        raise Exception(
            "The SPARQL query given to run_sparql must not contain an LIMIT clause"
        )

    def send_request(page: int) -> Response:
        paginated_sparql = sparql + f"LIMIT {PAGE_SIZE}\nOFFSET {page * PAGE_SIZE}"
        return request_triply_post(endpoint, paginated_sparql, triplydb_block_name)

    results = _run_query(send_request)
    if limit < 0:
        return results

    return islice(results, offset, offset + limit)


def _run_query(send_request_fn: Callable[[int], Response]) -> Iterable:
    """
    Common logic for the `run_saved_query` and `run_sparql` functions
    """
    logger = get_run_logger()
    page = 0
    prev = None

    while True:
        # Create and send the query
        response = send_request_fn(page)

        if response.text == prev:
            logger.info("Got duplicate results back, indicating the end of the dataset")
            break

        # Yield the items one by one
        json = response.json()
        for item in json:
            yield item

        if len(json) < PAGE_SIZE:
            logger.info(
                f"Got less results than PAGE_SIZE {PAGE_SIZE}, indicating of the end of the dataset"
            )
            break

        prev = response.text
        page += 1


@task
def request_triply_get(endpoint: str, triplydb_block_name: str) -> Response:
    """
    Send a GET request including the triply token to the given endpoint.
    """
    logger = get_run_logger()

    # Load credentials
    credentials = TriplyDBCredentials.load(triplydb_block_name)
    bearer_token = credentials.token.get_secret_value()

    # Send GET request
    headers = get_triply_headers(bearer_token)
    logger.info(f"Sending GET request to {endpoint}")
    response = requests.get(endpoint, headers=headers)

    if response.status_code != 200:
        logger.error(f"Status code {response.status_code} - {response.reason}")
        raise Exception("Request did not return status code 200")
    return response


@task
def request_triply_post(endpoint: str, body: str, triplydb_block_name: str) -> Response:
    """
    Send a POST request including the triply token to the given endpoint.
    """
    logger = get_run_logger()

    # Load credentials
    credentials = TriplyDBCredentials.load(triplydb_block_name)
    bearer_token = credentials.token.get_secret_value()

    # Send POST request
    headers = get_triply_headers(
        bearer_token,
        extra_headers={"Content-Type": "application/sparql-query"},
    )

    logger.info(f"Sending POST request to {endpoint}")
    response = requests.post(endpoint, headers=headers, data=body)

    if response.status_code != 200:
        logger.error(f"Status code {response.status_code} - {response.reason}")
        raise Exception("Request did not return status code 200")

    return response


def get_triply_headers(
    bearer_token: str, extra_headers: dict[str, str] | None = None
) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {bearer_token}",
    }
    extra_headers = extra_headers if extra_headers else {}
    return headers | extra_headers


def add_params_to_uri(uri: str, params: dict[str, Any]) -> str:
    encoded_params = urlencode(params)
    return f"{uri}?{encoded_params}" if "?" not in uri else f"{uri}&{encoded_params}"

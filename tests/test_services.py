from datetime import datetime
from unittest import mock

import pytest
from prefect import flow

from prefect_meemoo.services.tasks import sync_etl_service

get_request_count = 0

def mocked_requests_get(*args, **kwargs):
    global get_request_count
    get_request_count += 1
    class MockResponse:
        def __init__(self, json_data, status_code, text):
            self.json_data = json_data
            self.status_code = status_code
            self.text = text


        def json(self):
            return self.json_data

    print("get_request_count: ", get_request_count)
    if get_request_count == 1:
        return MockResponse({"job_running": True}, 200, "test post response")
    elif get_request_count == 2:
        return MockResponse({"job_running": False}, 200, "test post response")
    return MockResponse(None, 404, "test post response")

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, text):
            self.json_data = json_data
            self.status_code = status_code
            self.text = text

        def json(self):
            return self.json_data

    return MockResponse(None, 200, "test post response")

def mocked_get_run_logger():
    class MockLogger:
        def info(self, message):
            print(message)
    return MockLogger()

@mock.patch("prefect_meemoo.services.tasks.get_run_logger", side_effect=mocked_get_run_logger)
@mock.patch('prefect_meemoo.services.tasks.requests.post', side_effect=mocked_requests_post)
@mock.patch('prefect_meemoo.services.tasks.requests.get', side_effect=mocked_requests_get)
def test_run_sync_etl_service(mock_get, mock_post, mock_logger):
    result = sync_etl_service.fn(api_server="http://test", api_route="/sync/deewee", last_modified=None)
    assert isinstance(result, datetime)


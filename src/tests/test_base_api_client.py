import pytest
import os
import uuid
import json
from services.BaseAPIClient import BaseAPIClient
from services.AuthManager import AuthManager
from dotenv import dotenv_values


@pytest.fixture()
def request_headers() -> dict:
    return {
        "content-type": "application/vnd.api+json",
        "accept": "application/vnd.api+json",
        "x-correlation-id": str(uuid.uuid4()),
    }


@pytest.fixture()
def request_body() -> json:
    return {
        "messageReference": str(uuid.uuid4()),
        "recipient": {"nhsNumber": "9990548609", "dateOfBirth": "1982-03-17"},
        "originator": {"odsCode": "X26"},
        "personalisation": {"custom": "value"},
    }


class TestBaseAPIClient:
    def setup_method(self, method):
        print(f"Setting up test {method}")
        self.config = dotenv_values("../.env")
        self.base_api_client = BaseAPIClient(self.config.get("NHS_NOTIFY_BASE_URL"))
        self.access_token = AuthManager.get_access_token(self)
        request_headers["authorization"] = f"Bearer {self.access_token}"

    def teardown_method(self, method):
        print(f"Tearing down test {method}")

    def test_initialization(self):
        # Check base_url initialisation works as expected
        print()
        assert self.base_api_client.base_url == self.config.get("NHS_NOTIFY_BASE_URL")

    def test_make_request(self, request_body: json, request_headers: dict):

        response = self.base_api_client.make_request(
            method="POST",
            endpoint="/v1/messages",
            json=request_body,
            headers=request_headers,
        )
        print(response)
        assert response["status"] == 200
        # Assert the response status is 20X if the request is successful
        # Assert the endpoint is appended to the base_url correctly
        # Assert the response is returned and contains a parseable json object
        pass

    # def test_make_request_fail_response(self):
    #     #Assert the response status is 40X if the request fails
    #     pass

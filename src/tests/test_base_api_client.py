import pytest
import os
import uuid
import json
from services.BaseAPIClient import BaseAPIClient
from services.AuthManager import AuthManager
from unittest.mock import patch
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
        "data": {
            "type": "Message",
            "attributes": {
                "messageReference": str(uuid.uuid4()),
                "recipient": {"nhsNumber": "9990548609", "dateOfBirth": "1932-01-06"},
                "originator": {"odsCode": "X26"},
                "personalisation": {"custom": "value"},
            },
        }
    }


class TestBaseAPIClient:
    def setup_method(self, method):
        print(f"Setting up test {method}")
        self.config = dotenv_values("../.env")
        self.base_api_client = BaseAPIClient(self.config.get("NHS_NOTIFY_BASE_URL"))
        self.auth_manager = AuthManager()
        self.access_token = self.auth_manager.get_access_token()

    def teardown_method(self, method):
        print(f"Tearing down test {method}")

    ##### Potentially thinking these particular requests should be in a different test file
    # for specific endpoints to notify and auth headers, can translate those over if that's the case
    # In this file could potentially just make a basic API request to an endpoint that demonstrates the
    # BaseAPIClient can set up a URL and potentially an endpoint and make a request #####

    # Test init for BaseAPIClient works as intended
    def test_initialization(self):
        print()
        assert self.base_api_client.base_url == self.config.get("NHS_NOTIFY_BASE_URL")

    # Test successful request to notify (Do we need one for token request?)
    def test_make_request(self, request_body: json, request_headers: dict):
        request_headers["authorization"] = f"Bearer {self.access_token}"
        request_body["data"]["attributes"]["routingPlanId"] = self.config.get(
            "ROUTING_PLAN_ID"
        )
        response = self.base_api_client.make_request(
            method="POST",
            endpoint="/v1/messages",
            json=request_body,
            data=None,
            headers=request_headers,
        )
        responseJson = response.json()
        assert response.status_code == 201
        assert responseJson["data"]["type"] == "Message"

    # Test request should fail without auth header
    def test_make_request_missing_auth_header(
        self, request_body: json, request_headers: dict
    ):
        request_body["data"]["attributes"]["routingPlanId"] = self.config.get(
            "ROUTING_PLAN_ID"
        )
        response = self.base_api_client.make_request(
            method="POST",
            endpoint="/v1/messages",
            json=request_body,
            data=None,
            headers=request_headers,
        )
        responseJson = response.json()
        assert response.status_code == 401
        assert responseJson["errors"][0]["code"] == "CM_DENIED"

    # Test request should fail without routing_config_id
    def test_make_request_missing_routing_config_id(
        self, request_body: json, request_headers: dict
    ):
        request_headers["authorization"] = f"Bearer {self.access_token}"
        response = self.base_api_client.make_request(
            method="POST",
            endpoint="/v1/messages",
            json=request_body,
            data=None,
            headers=request_headers,
        )
        responseJson = response.json()
        print(responseJson)
        assert response.status_code == 400
        assert responseJson["errors"][0]["code"] == "CM_MISSING_VALUE"
        assert (
            responseJson["errors"][0]["source"]["pointer"]
            == "/data/attributes/routingPlanId"
        )

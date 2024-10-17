import json
from services.BaseAPIClient import BaseAPIClient
from services.AuthManager import AuthManager
import pytest


class TestBaseAPIClient:
    # Setup mainly for the notify specific functions, can change this to generic set-up if decided to switch
    def setup_method(
        self, method, nhs_notify_base_url="https://int.api.service.nhs.uk/comms"
    ):
        print(f"Setting up test {method}")
        self.base_api_client = BaseAPIClient(nhs_notify_base_url)
        self.auth_manager = AuthManager()
        self.access_token = self.auth_manager.get_access_token()

    def teardown_method(self, method):
        print(f"Tearing down test {method}")

    # Test init for BaseAPIClient works as intended
    def test_initialization_generic(self):
        self.base_api_client.base_url = "https://reqres.in"
        assert self.base_api_client.base_url == "https://reqres.in"

    # Test to show the make_request function can combine base_urls and endpoints to make a request
    def test_make_request_generic(self, mocker, test_generic_api_response):
        self.base_api_client.base_url = "https://reqres.in"

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = test_generic_api_response
        mocker.patch("requests.request", return_value=mock_response)

        response = self.base_api_client.make_request(
            method="GET",
            endpoint="/api/users",
            data=None,
            json=None,
            headers=None,
            params=None,
        )
        responseJson = response.json()
        assert response.status_code == 200
        assert responseJson["page"] == 1

    def test_make_request_generic_incorrect_endpoint(self, mocker):
        self.base_api_client.base_url = "https://reqres.in"

        mock_response = mocker.MagicMock()
        mock_response.status_code = 404
        mocker.patch("requests.request", return_value=mock_response)

        response = self.base_api_client.make_request(
            method="GET",
            endpoint="/foo/bar",
            data=None,
            json=None,
            headers=None,
            params=None,
        )
        assert response.status_code == 404

    ##### Potentially thinking these particular requests below should be in a different test file
    # for specific endpoints to notify and auth headers, can translate those over if that's the case
    # In this file could potentially just make a basic API request to an endpoint that demonstrates the
    # BaseAPIClient can set up a URL and potentially an endpoint and make a request #####

    # def test_initialization(self, nhs_notify_base_url):
    #     assert self.base_api_client.base_url == nhs_notify_base_url

    # # Test successful request to notify (Do we need one for token request?)
    # def test_make_request(
    #     self, request_body: json, request_headers: dict, routing_config_id: str
    # ):
    #     request_headers["authorization"] = f"Bearer {self.access_token}"
    #     request_body["data"]["attributes"]["routingPlanId"] = routing_config_id
    #     response = self.base_api_client.make_request(
    #         method="POST",
    #         endpoint="/v1/messages",
    #         json=request_body,
    #         data=None,
    #         headers=request_headers,
    #     )
    #     responseJson = response.json()
    #     assert response.status_code == 201
    #     assert responseJson["data"]["type"] == "Message"

    # # Test request should fail without auth header
    # def test_make_request_missing_auth_header(
    #     self, request_body: json, request_headers: dict, routing_config_id
    # ):
    #     request_body["data"]["attributes"]["routingPlanId"] = routing_config_id
    #     response = self.base_api_client.make_request(
    #         method="POST",
    #         endpoint="/v1/messages",
    #         json=request_body,
    #         data=None,
    #         headers=request_headers,
    #     )
    #     responseJson = response.json()
    #     assert response.status_code == 401
    #     assert responseJson["errors"][0]["code"] == "CM_DENIED"

    # # Test request should fail without routing_config_id
    # def test_make_request_missing_routing_config_id(
    #     self, request_body: json, request_headers: dict
    # ):
    #     request_headers["authorization"] = f"Bearer {self.access_token}"
    #     response = self.base_api_client.make_request(
    #         method="POST",
    #         endpoint="/v1/messages",
    #         json=request_body,
    #         data=None,
    #         headers=request_headers,
    #     )
    #     responseJson = response.json()
    #     assert response.status_code == 400
    #     assert responseJson["errors"][0]["code"] == "CM_MISSING_VALUE"
    #     assert (
    #         responseJson["errors"][0]["source"]["pointer"]
    #         == "/data/attributes/routingPlanId"
    #     )

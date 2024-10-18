class TestBaseAPIClient:
    # Do we need to mock the API calls when we are supposed to be testing the API calls work, or is this worth mocking
    # And then just test that the url+endpoint formation works together?

    # Test init for BaseAPIClient works as intended
    def test_initialization(self, generic_base_api_client):
        assert generic_base_api_client.base_url == "https://reqres.in"

    # Test to show the make_request function can combine base_urls and endpoints to make a request
    def test_make_request(self, generic_base_api_client):
        # mocker, test_generic_api_response
        # mock_response = mocker.MagicMock()
        # mock_response.status_code = 200
        # mock_response.json.return_value = test_generic_api_response
        # mocker.patch("requests.request", return_value=mock_response)
        response = generic_base_api_client.make_request(
            method="GET",
            endpoint="/api/users",
            data=None,
            json=None,
            headers=None,
            params=None,
        )
        responseJson = response.json()
        assert response.status_code == 200
        assert response.url == "https://reqres.in/api/users"
        assert responseJson["page"] == 1

    def test_make_request_generic_incorrect_endpoint(self, generic_base_api_client):
        response = generic_base_api_client.make_request(
            method="GET",
            endpoint="/foo/bar",
            data=None,
            json=None,
            headers=None,
            params=None,
        )
        assert response.status_code == 404

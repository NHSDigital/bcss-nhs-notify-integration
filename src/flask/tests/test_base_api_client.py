class TestBaseAPIClient:
    # Test init for BaseAPIClient works as intended
    def test_initialization(self, generic_base_api_client):
        assert generic_base_api_client.base_url == "https://reqres.in"

    # Test to show the make_request function can combine base_urls and endpoints to make a request
    def test_make_request(self, generic_base_api_client):
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

    # Test to make a request to an incorrect endpoint and expect a 404 if incorrectly formatted
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

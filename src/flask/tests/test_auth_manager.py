from dotenv import dotenv_values
from services.AuthManager import AuthManager


class TestAuthManager:
    def setup_method(self, method):
        print(f"Setting up test {method}")
        self.auth_manager = AuthManager()

    def teardown_method(self, method):
        print(f"Tearing down test {method}")

    # Test the init dunder of the class
    def test_initialization(self, token_url):
        # Only setup is baseapi client, and if this is mocked is this needed?
        assert self.auth_manager.api_client.base_url == token_url

    # Test JWT gen, make sure its a legit JWT? probably a library for that
    def test_jwt_gen_setup(self):
        # Check local envs work, compare their values to the ones in personal .env file, use a config dotenv to pull out
        pass

    def test_access_token_request_fail_jwt(self):
        # Assert failure when JWT is incorrect/missing
        pass

    # Test access token request, expect a 20X response with everything correct
    def test_access_token_request(self):
        # Mock JWT gen, mocks the actual request? Get the access token field from the mocked response and if so, pass
        pass

    def test_access_token_request_fail_token_missing(self):
        # Assert failure when token is missing from response
        pass

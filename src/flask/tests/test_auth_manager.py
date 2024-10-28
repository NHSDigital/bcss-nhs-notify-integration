from services.util import Util


class TestAuthManager:
    # Test init for AuthManager works as intended
    def test_initialization(
        self,
        auth_manager,
        token_url,
    ):
        assert auth_manager.api_client.base_url == token_url

    # Test access token request, expect a 20X response with everything correct
    def test_get_access_token(
        self,
        mocker,
        auth_manager,
        test_get_access_token_mock_response,
        test_jwt,
        test_private_key,
    ):

        mocker.patch.object(
            auth_manager.api_client,
            "make_request",
            return_value=test_get_access_token_mock_response,
        )
        mocker.patch.object(auth_manager, "generate_auth_jwt", return_value=test_jwt)

        response = auth_manager.get_access_token()
        assert response == test_get_access_token_mock_response["access_token"]

    # Test JWT gen function, expect to return mocked JWT token from Util
    def test_generate_auth_jwt(self, mocker, auth_manager, test_jwt, test_private_key):

        mocker.patch.object(Util, "generate_jwt", return_value=test_jwt)
        mocker.patch.object(Util, "get_private_key", return_value=test_private_key)

        response = auth_manager.generate_auth_jwt()
        assert response == test_jwt

import pytest


class TestUtil:
    def test_generate_message(self):
        # Assert returned message to example message (load in from test examples folder?)
        pass

    def test_generate_single_message_request_body(self):
        # Mock the generate message? Just use the actual function
        # Assert end result to full example single message (load in from test examples folder?)
        pass

    def test_generate_batch_message_request_body(self):
        # Mock the generate message? Just use the actual function
        # Assert end result to full example batch message (load in from test examples folder?)
        pass

    def test_get_private_key(self):
        # Can read a private key from a file, assert the private key variable contents match the test file
        # (load in from test examples folder?)
        pass

    def test_generate_jwt(self):
        # Expect a JWT to be generated, check if its a valid JWT,
        pass

    def test_generate_jwt_fail_private_key(self):
        # Pass in incorrect/missing private key and expect a failure
        pass

    def test_generate_jwt_fail_kid(self):
        # Pass in incorrect/missing KID and expect a failure
        pass

    def test_generate_jwt_fail_api_key(self):
        # Pass in incorrect/missing API_KEY and expect a failure
        pass

    def test_generate_jwt_fail_token_url(self):
        # Pass in incorrect/missing TOKEN_URL and expect a failure
        pass

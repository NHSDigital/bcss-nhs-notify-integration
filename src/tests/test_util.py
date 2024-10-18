from services.Util import Util
import jwt
import json
import pytest


class TestUtil:

    # Assert returned message to example message (load in from test examples/conftest fixture?)
    def test_generate_message(
        self, test_recipient: dict, test_notify_message_base: json
    ):
        # Assert returned message to example message
        message_base = Util.generate_message(test_recipient)
        assert message_base["recipient"]["nhsNumber"] == "9990548609"
        assert message_base["recipient"]["dateOfBirth"] == "1932-01-06"
        # assert message_base == test_notify_message_base - need a way to handle UUIDs?

    def test_generate_single_message_request_body(self, test_recipient):
        message_request_single = Util.generate_single_message_request_body(
            test_recipient, "test_routing_config_id"
        )
        # Assert end result to full example single message (load in from test examples folder?)
        assert message_request_single["data"]["type"] == "Message"
        assert (
            message_request_single["data"]["attributes"]["routingPlanId"]
            == "test_routing_config_id"
        )
        # assert message_request_single == test_notify_message_single - need a way to handle UUIDs?

    def test_generate_batch_message_request_body(self, test_recipient):
        message_request_batch = Util.generate_batch_message_request_body(
            "test_routing_config_id", "test_message_batch_reference", [test_recipient]
        )
        assert message_request_batch["data"]["type"] == "MessageBatch"
        assert (
            message_request_batch["data"]["attributes"]["routingPlanId"]
            == "test_routing_config_id"
        )
        assert (
            message_request_batch["data"]["attributes"]["messageBatchReference"]
            == "test_message_batch_reference"
        )
        # Assert end result to full example batch message (load in from test examples folder?)
        pass

    def test_get_private_key(self):
        test_private_key = Util.get_private_key("test_private_key.key")
        assert test_private_key == "test_private_key\n"
        # Can read a private key from a file, assert the private key variable contents match the test file
        # (load in from test examples folder?)
        pass

    def test_generate_jwt(self, test_jwt_params):
        test_private_key = Util.get_private_key("../jwtRS512.key")
        test_jwt = Util.generate_jwt(
            test_jwt_params["algorithm"],
            test_private_key,
            test_jwt_params["headers"],
            test_jwt_params["payload"],
            test_jwt_params["expiry_minutes"],
        )
        # Expect a JWT to be generated, check if its a valid JWT,
        pass

    def test_generate_jwt_fail_private_key_format(self, test_jwt_params):
        with pytest.raises(TypeError) as exception:
            Util.generate_jwt(
                test_jwt_params["algorithm"],
                None,
                test_jwt_params["headers"],
                test_jwt_params["payload"],
                test_jwt_params["expiry_minutes"],
            )
        assert "Expecting a PEM-formatted key." in str(exception)
        # Pass in incorrect/missing private key and expect a failure

    def test_generate_jwt_fail_kid_format(self, test_jwt_params):
        with pytest.raises(jwt.InvalidTokenError) as exception:
            test_private_key = Util.get_private_key("../jwtRS512.key")
            test_jwt_params["headers"]["kid"] = None
            Util.generate_jwt(
                test_jwt_params["algorithm"],
                test_private_key,
                test_jwt_params["headers"],
                test_jwt_params["payload"],
                test_jwt_params["expiry_minutes"],
            )
        assert "Key ID header parameter must be a string" in str(exception)
        # Pass in incorrect/missing KID and expect a failure

    #### Could add tests to then decode the returned JWT to check the contents are "null" where the missing info was
    #### Aud/ISS/Sub, even Algorithm?
    def test_generate_jwt_null_token_url(self, test_jwt_params):
        test_private_key = Util.get_private_key("../jwtRS512.key")
        test_jwt_params["payload"]["aud"] = None
        test_jwt = Util.generate_jwt(
            test_jwt_params["algorithm"],
            test_private_key,
            test_jwt_params["headers"],
            test_jwt_params["payload"],
            test_jwt_params["expiry_minutes"],
        )
        # Decode test_jwt using the public key
        # Assert that the aud is null if possible?
        pass

    def test_generate_jwt_null_api_keys(self, test_jwt_params):
        test_private_key = Util.get_private_key("../jwtRS512.key")
        test_jwt_params["payload"]["aud"] = None
        test_jwt = Util.generate_jwt(
            test_jwt_params["algorithm"],
            test_private_key,
            test_jwt_params["headers"],
            test_jwt_params["payload"],
            test_jwt_params["expiry_minutes"],
        )
        # Decode test_jwt using the public key
        # Assert that the sub and iss is null if possible?
        pass

    def test_generate_jwt_null_algorithm(self, test_jwt_params):
        test_private_key = Util.get_private_key("../jwtRS512.key")
        test_jwt_params["payload"]["aud"] = None
        test_jwt_params["headers"]["alg"] = None
        test_jwt = Util.generate_jwt(
            test_jwt_params["algorithm"],
            test_private_key,
            test_jwt_params["headers"],
            test_jwt_params["payload"],
            test_jwt_params["expiry_minutes"],
        )
        # Decode test_jwt using the public key
        # Assert that the algorithm is null if possible?
        pass

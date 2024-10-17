from services.Util import Util
import json


class TestUtil:

    # Assert returned message to example message (load in from test examples/conftest fixture?)
    def test_generate_message(
        self, test_recipient: dict, test_notify_message_base: json
    ):
        # Assert returned message to example message
        message_base = Util.generate_message(test_recipient)
        assert message_base["recipient"]["nhsNumber"] == "9990548609"
        assert message_base["recipient"]["dateOfBirth"] == "1932-01-06"
        # assert message_base == test_notify_message_base - currently need a way to handle UUIDs

    def test_generate_single_message_request_body(
        self, test_recipient, test_notify_message_single
    ):
        message_request_single = Util.generate_single_message_request_body(
            test_recipient, "test_routing_config_id"
        )
        # Assert end result to full example single message (load in from test examples folder?)
        assert message_request_single["data"]["type"] == "Message"
        assert (
            message_request_single["data"]["attributes"]["routingPlanId"]
            == "test_routing_config_id"
        )
        # assert message_request_single == test_notify_message_single - currently need a way to handle UUIDs

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

    def test_generate_jwt(self):
        # test_jwt = Util.generate_jwt("RS
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

from services.NHSNotify import NHSNotify
from services.Util import Util


class TestNHSNotify:
    def setup_method(
        self, method, nhs_notify_base_url="https://int.api.service.nhs.uk/comms"
    ):
        print(f"Setting up test {method}")
        self.nhs_notify = NHSNotify(nhs_notify_base_url)

    def teardown_method(self, method):
        print(f"Tearing down test {method}")

    def test_initialization(self, base_api_client_notify):
        assert self.nhs_notify.api_client.base_url == base_api_client_notify.base_url
        pass

    # Mocked Util and Request functions
    def test_send_single_message(
        self,
        mocker,
        test_recipient,
        generate_notify_single_mock_response,
        single_message_request_mock_response,
    ):
        test_routing_config_id = "test_routing_config_id"

        util = Util()
        mocker.patch.object(
            util,
            "generate_single_message_request_body",
            return_value=generate_notify_single_mock_response,
        )

        mock_response = mocker.MagicMock()
        mock_response.json.return_value = single_message_request_mock_response
        mocker.patch.object(
            self.nhs_notify.api_client, "make_request", return_value=mock_response
        )

        response = self.nhs_notify.send_single_message(
            "test_access_token",
            test_routing_config_id,
            test_recipient,
        )
        assert type(response) == dict
        assert response["data"]["type"] == "Message"
        assert (
            response["data"]["attributes"]["routingPlan"]["id"]
            == test_routing_config_id
        )
        # Correct setup correct access token, mock correct request body

    def test_send_batch_message(
        self,
        mocker,
        test_recipient_batch,
        generate_notify_batch_mock_response,
        batch_message_request_mock_response,
    ):
        test_routing_config_id = "test_routing_config_id"

        util = Util()
        mocker.patch.object(
            util,
            "generate_batch_message_request_body",
            return_value=generate_notify_batch_mock_response,
        )

        mock_response = mocker.MagicMock()
        mock_response.json.return_value = batch_message_request_mock_response
        mocker.patch.object(
            self.nhs_notify.api_client, "make_request", return_value=mock_response
        )

        response = self.nhs_notify.send_batch_message(
            "test_access_token",
            test_routing_config_id,
            test_recipient_batch,
        )
        assert response["data"]["type"] == "MessageBatch"
        assert (
            response["data"]["attributes"]["routingPlan"]["id"]
            == test_routing_config_id
        )

    # Test request should fail without auth header
    def test_make_request_missing_auth_header(
        self,
        mocker,
        test_recipient,
        generate_notify_single_mock_response,
        notify_missing_auth_request_mock_response,
    ):
        test_routing_config_id = "test_routing_config_id"

        util = Util()
        mocker.patch.object(
            util,
            "generate_single_message_request_body",
            return_value=generate_notify_single_mock_response,
        )

        mock_response = mocker.MagicMock()
        mock_response.json.return_value = notify_missing_auth_request_mock_response
        mocker.patch.object(
            self.nhs_notify.api_client, "make_request", return_value=mock_response
        )

        response = self.nhs_notify.send_single_message(
            "test_access_token",
            test_routing_config_id,
            test_recipient,
        )
        assert response["errors"][0]["status"] == "401"
        assert response["errors"][0]["code"] == "CM_DENIED"

    # Test request should fail without routing_config_id
    def test_make_request_incorrect_routing_config(
        self,
        mocker,
        test_recipient,
        generate_notify_single_mock_response,
        notify_incorrect_routing_config_request_mock_response,
    ):

        util = Util()
        mocker.patch.object(
            util,
            "generate_single_message_request_body",
            return_value=generate_notify_single_mock_response,
        )

        mock_response = mocker.MagicMock()
        mock_response.json.return_value = (
            notify_incorrect_routing_config_request_mock_response
        )
        mocker.patch.object(
            self.nhs_notify.api_client, "make_request", return_value=mock_response
        )

        response = self.nhs_notify.send_single_message(
            "test_access_token",
            "",
            test_recipient,
        )
        assert response["errors"][0]["status"] == "400"
        assert response["errors"][0]["code"] == "CM_INVALID_VALUE"

    # Test for empty recipients list
    def test_make_request_empty_recipients(
        self,
        mocker,
        generate_notify_single_mock_response,
        notify_empty_recipients_request_mock_response,
    ):

        util = Util()
        mocker.patch.object(
            util,
            "generate_single_message_request_body",
            return_value=generate_notify_single_mock_response,
        )

        mock_response = mocker.MagicMock()
        mock_response.json.return_value = notify_empty_recipients_request_mock_response
        mocker.patch.object(
            self.nhs_notify.api_client, "make_request", return_value=mock_response
        )

        response = self.nhs_notify.send_single_message(
            "test_access_token",
            "test_routing_config_id",
            [],
        )
        assert response["errors"][0]["status"] == "400"
        assert response["errors"][0]["code"] == "CM_INVALID_VALUE"


####################################################################################################
# def test_get_message_status(self):
#     # Correct setup correct access token, mock correct request body
#     # Mock request
#     pass

# def test_get_message_status_fail_access_token(self):
#     # Incorrect/missing access token
#     # Mock request
#     pass

# def test_get_NHS_account_details(self):
#     # Correct setup correct access token, mock correct request body
#     # Mock request
#     pass

# def test_get_NHS_account_details_fail_access_token(self):
#     # Incorrect/missing access token
#     # Mock request
#     pass

# def test_get_NHS_account_details_fail_ods_code(self):
#     # Incorrect/missing ods code
#     # Mock request
#     pass

# def test_get_NHS_account_details_fail_resource_missing(self):
#     # Force a 404 response
#     # Mock request
#     pass

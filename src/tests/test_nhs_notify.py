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
        routing_config_id,
        test_recipient,
        generate_notify_single_mock_response,
        single_message_request_mock_response,
    ):

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
            routing_config_id,
            test_recipient,
        )
        assert type(response) == dict
        assert response["data"]["attributes"]["messageStatus"] == "created"
        assert response["data"]["attributes"]["routingPlan"]["id"] == routing_config_id

        # Correct setup correct access token, mock correct request body
        # Mock request
        pass

    #### Keep working on this one after updating index
    def test_send_batch_message(
        self,
        mocker,
        routing_config_id,
        test_recipient,
        generate_notify_batch_mock_response,
        batch_message_request_mock_response,
    ):

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
            routing_config_id,
            test_recipient,
        )
        assert type(response) == dict
        assert response["data"]["attributes"]["messageStatus"] == "created"
        assert response["data"]["attributes"]["routingPlan"]["id"] == routing_config_id
        # Incorrect/missing access token
        # Mock request
        pass

    def test_send_single_message_fail_request_body(self):
        # Incorrect/missing request body
        # Mock request
        pass

    def test_send_single_message_fail_access_token(self):
        # Correct setup correct access token, mock correct request body
        # Mock request
        pass

    def test_send_batch_message_fail_access_token(self):
        # Incorrect/missing access token
        # Mock request
        pass

    def test_send_batch_message_fail_request_body(self):
        # Incorrect/missing request body
        # Mock request
        pass

    def test_get_message_status(self):
        # Correct setup correct access token, mock correct request body
        # Mock request
        pass

    def test_get_message_status_fail_access_token(self):
        # Incorrect/missing access token
        # Mock request
        pass

    def test_get_NHS_account_details(self):
        # Correct setup correct access token, mock correct request body
        # Mock request
        pass

    def test_get_NHS_account_details_fail_access_token(self):
        # Incorrect/missing access token
        # Mock request
        pass

    def test_get_NHS_account_details_fail_ods_code(self):
        # Incorrect/missing ods code
        # Mock request
        pass

    def test_get_NHS_account_details_fail_resource_missing(self):
        # Force a 404 response
        # Mock request
        pass

from services.util import Util


class TestNHSNotify:
    # Test init for BaseAPIClient works as intended
    def test_initialization(self, nhs_notify, nhs_notify_base_url):
        assert nhs_notify.api_client.base_url == nhs_notify_base_url

    # Test to send a single message
    def test_send_single_message(
        self,
        mocker,
        nhs_notify,
        test_recipient,
        test_access_token,
        generate_notify_single_mock_response,
        single_message_request_mock_response,
    ):
        test_routing_config_id = "test_routing_config_id"

        mocker.patch.object(
            Util,
            "generate_single_message_request_body",
            return_value=generate_notify_single_mock_response,
        )

        mocker.patch.object(
            nhs_notify.api_client,
            "make_request",
            return_value=single_message_request_mock_response,
        )

        response = nhs_notify.send_single_message(
            test_access_token,
            test_routing_config_id,
            test_recipient,
        )

        assert response == single_message_request_mock_response

    # Test to send a batch message
    def test_send_batch_message(
        self,
        mocker,
        nhs_notify,
        test_recipient_batch,
        test_access_token,
        generate_notify_batch_mock_response,
        batch_message_request_mock_response,
    ):
        test_routing_config_id = "test_routing_config_id"

        mocker.patch.object(
            Util,
            "generate_batch_message_request_body",
            return_value=generate_notify_batch_mock_response,
        )

        mocker.patch.object(
            nhs_notify.api_client,
            "make_request",
            return_value=batch_message_request_mock_response,
        )

        response = nhs_notify.send_batch_message(
            test_access_token,
            test_routing_config_id,
            test_recipient_batch,
        )

        assert response == batch_message_request_mock_response

    # Test request should fail without auth header
    def test_make_request_missing_auth_header(
        self,
        mocker,
        nhs_notify,
        test_recipient,
        test_access_token,
        generate_notify_single_mock_response,
        notify_401_missing_auth_request_mock_response,
    ):
        test_routing_config_id = "test_routing_config_id"

        mocker.patch.object(
            Util,
            "generate_single_message_request_body",
            return_value=generate_notify_single_mock_response,
        )

        mocker.patch.object(
            nhs_notify.api_client,
            "make_request",
            return_value=notify_401_missing_auth_request_mock_response,
        )

        response = nhs_notify.send_single_message(
            test_access_token,
            test_routing_config_id,
            test_recipient,
        )

        assert response == notify_401_missing_auth_request_mock_response

    # Test request should fail without routing_config_id
    def test_make_request_incorrect_routing_config(
        self,
        mocker,
        nhs_notify,
        test_recipient,
        test_access_token,
        generate_notify_single_mock_response,
        notify_400_incorrect_routing_config_request_mock_response,
    ):

        mocker.patch.object(
            Util,
            "generate_single_message_request_body",
            return_value=generate_notify_single_mock_response,
        )

        mocker.patch.object(
            nhs_notify.api_client,
            "make_request",
            return_value=notify_400_incorrect_routing_config_request_mock_response,
        )

        response = nhs_notify.send_single_message(
            test_access_token,
            "",
            test_recipient,
        )
        assert response == notify_400_incorrect_routing_config_request_mock_response

    # Test successful get message status request
    def test_get_message_status(
        self,
        mocker,
        nhs_notify,
        test_message_id,
        test_access_token,
        notify_get_message_status_response,
    ):

        mocker.patch.object(
            nhs_notify.api_client,
            "make_request",
            return_value=notify_get_message_status_response,
        )

        response = nhs_notify.get_message_status(test_access_token, test_message_id)

        assert response == notify_get_message_status_response

    # Test to get message status with missing message id
    def test_get_message_status_missing_id(
        self,
        mocker,
        nhs_notify,
        test_access_token,
        notify_403_forbidden_response,
    ):

        mocker.patch.object(
            nhs_notify.api_client,
            "make_request",
            return_value=notify_403_forbidden_response,
        )

        response = nhs_notify.get_message_status(test_access_token, "")

        assert response == notify_403_forbidden_response

    # Test for successful get nhs account details request
    def test_get_nhs_account_details(
        self,
        mocker,
        nhs_notify,
        notify_get_nhs_app_account_details_mock_response,
        test_ods_code,
        test_access_token,
    ):

        mocker.patch.object(
            nhs_notify.api_client,
            "make_request",
            return_value=notify_get_nhs_app_account_details_mock_response,
        )

        response = nhs_notify.get_nhs_account_details(
            test_access_token, test_ods_code, "1"
        )

        assert response == notify_get_nhs_app_account_details_mock_response

    # Test to fail for get nhs account details with missing ods code
    def test_get_nhs_account_details_missing_ods_code(
        self,
        mocker,
        nhs_notify,
        notify_400_missing_ods_code_response,
        test_access_token,
    ):

        mocker.patch.object(
            nhs_notify.api_client,
            "make_request",
            return_value=notify_400_missing_ods_code_response,
        )

        response = nhs_notify.get_nhs_account_details(test_access_token, "", "1")

        assert response == notify_400_missing_ods_code_response

class TestBCSSCommsManager:
    # Test init for BCSSCommsManager works as intended
    def test_initialization(
        self,
        bcss_comms_manager,
        nhs_notify,
        auth_manager,
        data_access,
    ):
        assert bcss_comms_manager.nhs_notify == nhs_notify
        assert bcss_comms_manager.auth_manager == auth_manager
        assert bcss_comms_manager.data_access == data_access

    # Test to send pre-invitation to single recipient with correct data inputted
    def test_send_pre_invitation_single(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient,
        test_routing_config_id,
        test_access_token,
        single_message_request_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_single_message",
            return_value=single_message_request_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation(
            test_routing_config_id, [test_recipient]
        )

        assert response == single_message_request_mock_response

    # Test to send pre-invitation to batch with correct data inputted
    def test_send_pre_invitation_batch(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient_batch,
        test_routing_config_id,
        test_access_token,
        batch_message_request_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_batch_message",
            return_value=batch_message_request_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation(
            test_routing_config_id, test_recipient_batch
        )

        assert response == batch_message_request_mock_response

    # TEMPORARY MISSING ROUTING CONFIG ID TEST, ADD HANDLING FOR MISSING ROUTING CONFIG ID AND RECIPIENTS
    # TO OUR COMMS MANAGER
    # Test to send pre-invitation to single recipient with missing routing config id
    def test_send_pre_invitation_single_missing_routing_config(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient,
        test_access_token,
        notify_400_incorrect_routing_config_request_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_single_message",
            return_value=notify_400_incorrect_routing_config_request_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation("", [test_recipient])

        assert response == notify_400_incorrect_routing_config_request_mock_response

    # Test to send pre-invitation to batch with missing routing config id
    def test_send_pre_invitation_batch_missing_routing_config(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient_batch,
        test_access_token,
        notify_400_incorrect_routing_config_request_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_batch_message",
            return_value=notify_400_incorrect_routing_config_request_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation("", test_recipient_batch)

        assert response == notify_400_incorrect_routing_config_request_mock_response

    # Test to send pre-invitation to single recipient with missing NHS number as ""
    def test_send_pre_invitation_missing_recipient_nhs_number(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient_missing_nhs_number,
        test_routing_config_id,
        test_access_token,
        notify_400_missing_nhs_number_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        # Currently batch but realistically should throw error as soon as it realises no recipient number
        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_single_message",
            return_value=notify_400_missing_nhs_number_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation(
            test_routing_config_id, [test_recipient_missing_nhs_number]
        )

        assert response == notify_400_missing_nhs_number_mock_response

    # Test to send pre-invitation to single recipient with missing recipient DOB as ""
    def test_send_pre_invitation_missing_recipient_dob(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient_missing_dob,
        test_routing_config_id,
        test_access_token,
        notify_400_missing_dob_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        # Currently batch but realistically should throw error as soon as it realises no recipient number
        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_single_message",
            return_value=notify_400_missing_dob_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation(
            test_routing_config_id, [test_recipient_missing_dob]
        )

        assert response == notify_400_missing_dob_mock_response

    def test_get_message_status(
        self,
        mocker,
        bcss_comms_manager,
        test_message_id,
        test_access_token,
        notify_get_message_status_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "get_message_status",
            return_value=notify_get_message_status_response,
        )

        response = bcss_comms_manager.get_message_status(test_message_id)

        assert response == notify_get_message_status_response

    # Test to get message status with missing message id, LIKELY NEEDS TO BE HANDLED BY
    # BCSSCOMMSMANAGER BEFORE REACHING FURTHER
    def test_get_message_status_missing_id(
        self,
        mocker,
        bcss_comms_manager,
        notify_403_forbidden_response,
        test_access_token,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "get_message_status",
            return_value=notify_403_forbidden_response,
        )

        response = bcss_comms_manager.get_message_status("")

        assert response == notify_403_forbidden_response

    def test_get_nhs_app_account_details(
        self,
        mocker,
        bcss_comms_manager,
        test_access_token,
        notify_get_nhs_app_account_details_mock_response,
        test_ODS_code,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "get_NHS_account_details",
            return_value=notify_get_nhs_app_account_details_mock_response,
        )

        response = bcss_comms_manager.get_nhs_app_account_details(test_ODS_code, "1")

        assert response == notify_get_nhs_app_account_details_mock_response

    def test_get_nhs_app_account_details_missing_ods_code(
        self,
        mocker,
        bcss_comms_manager,
        test_access_token,
        notify_400_missing_ods_code_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value=test_access_token,
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "get_NHS_account_details",
            return_value=notify_400_missing_ods_code_response,
        )

        response = bcss_comms_manager.get_nhs_app_account_details("", "1")

        assert response == notify_400_missing_ods_code_response

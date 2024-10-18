class TestBCSSCommsManager:
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
        single_message_request_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value="test_access_token",
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

        assert type(response) == dict
        assert response["data"]["type"] == "Message"
        assert (
            response["data"]["attributes"]["routingPlan"]["id"]
            == test_routing_config_id
        )

    # TEMPORARY MISSING ROUTING CONFIG ID TEST, ADD HANDLING FOR MISSING ROUTING CONFIG ID AND RECIPIENTS
    # TO OUR COMMS MANAGER
    # Test to send pre-invitation to single recipient with missing routing config id
    def test_send_pre_invitation_single_missing_routing_config(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient,
        notify_incorrect_routing_config_request_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value="test_access_token",
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_single_message",
            return_value=notify_incorrect_routing_config_request_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation("", [test_recipient])

        assert response["errors"][0]["status"] == "400"
        assert response["errors"][0]["code"] == "CM_INVALID_VALUE"

    # Test to send pre-invitation to batch with correct data inputted
    def test_send_pre_invitation_batch(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient_batch,
        test_routing_config_id,
        batch_message_request_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value="test_access_token",
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

        assert type(response) == dict
        assert response["data"]["type"] == "MessageBatch"
        assert (
            response["data"]["attributes"]["routingPlan"]["id"]
            == test_routing_config_id
        )

    # Test to send pre-invitation to batch with missing routing config id
    def test_send_pre_invitation_batch_missing_routing_config(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient_batch,
        notify_incorrect_routing_config_request_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value="test_access_token",
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_batch_message",
            return_value=notify_incorrect_routing_config_request_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation("", test_recipient_batch)

        assert response["errors"][0]["status"] == "400"
        assert response["errors"][0]["code"] == "CM_INVALID_VALUE"
        assert (
            response["errors"][0]["source"]["pointer"]
            == "/data/attributes/routingPlanId"
        )

    # Test to send pre-invitation to single recipient with missing NHS number as ""
    def test_send_pre_invitation_missing_recipient_nhs_number(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient_missing_nhs_number,
        test_routing_config_id,
        notify_missing_nhs_number_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value="test_access_token",
        )

        # Currently batch but realistically should throw error as soon as it realises no recipient number
        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_single_message",
            return_value=notify_missing_nhs_number_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation(
            test_routing_config_id, [test_recipient_missing_nhs_number]
        )

        assert response["errors"][0]["status"] == "400"
        assert response["errors"][0]["code"] == "CM_INVALID_NHS_NUMBER"
        assert (
            response["errors"][0]["source"]["pointer"]
            == "/data/attributes/recipient/nhsNumber"
        )

    # Test to send pre-invitation to single recipient with missing recipient DOB as ""
    def test_send_pre_invitation_missing_recipient_dob(
        self,
        mocker,
        bcss_comms_manager,
        test_recipient_missing_dob,
        test_routing_config_id,
        notify_missing_dob_mock_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value="test_access_token",
        )

        # Currently batch but realistically should throw error as soon as it realises no recipient number
        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "send_single_message",
            return_value=notify_missing_dob_mock_response,
        )

        mocker.patch.object(bcss_comms_manager.data_access, "create_data")

        response = bcss_comms_manager.send_pre_invitation(
            test_routing_config_id, [test_recipient_missing_dob]
        )

        assert response["errors"][0]["status"] == "400"
        assert response["errors"][0]["code"] == "CM_INVALID_VALUE"
        assert (
            response["errors"][0]["source"]["pointer"]
            == "/data/attributes/recipient/dateOfBirth"
        )

    def test_get_message_status(
        self,
        mocker,
        bcss_comms_manager,
        test_message_id,
        notify_get_message_status_response,
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value="test_access_token",
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "get_message_status",
            return_value=notify_get_message_status_response,
        )

        response = bcss_comms_manager.get_message_status(test_message_id)

        assert type(response) == dict
        assert response["data"]["type"] == "Message"
        assert response["data"]["id"] == test_message_id
        assert response["data"]["attributes"]["messageStatus"] == "pending_enrichment"

    # Test to get message status with missing message id, LIKELY NEEDS TO BE HANDLED BY
    # BCSSCOMMSMANAGER BEFORE REACHING FURTHER
    def test_get_message_status_missing_id(
        self, mocker, bcss_comms_manager, notify_get_message_status_response
    ):

        mocker.patch.object(
            bcss_comms_manager.auth_manager,
            "get_access_token",
            return_value="test_access_token",
        )

        mocker.patch.object(
            bcss_comms_manager.nhs_notify,
            "get_message_status",
            return_value=notify_get_message_status_response,
        )

        response = bcss_comms_manager.get_message_status("")

        assert response["errors"][0]["status"] == "403"
        assert response["errors"][0]["code"] == "CM_FORBIDDEN"

    def test_get_nhs_app_account_details(self):
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

    def test_get_nhs_app_account_details_missing_ods_code(self):
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

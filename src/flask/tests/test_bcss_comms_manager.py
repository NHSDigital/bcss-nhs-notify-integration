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
        # recipients length > 1
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

    def test_send_pre_invitation_batch_missing_routing_config(self):
        # recipients length > 1
        # no routing config id
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

    def test_send_pre_invitation_missing_recipients(self):
        # recipients length = 0
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

    def test_get_message_status(self):
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

    def test_get_message_status_missing_id(self):
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

    def test_get_nhs_app_account_details(self):
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

    def test_get_nhs_app_account_details_missing_ods_code(self):
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

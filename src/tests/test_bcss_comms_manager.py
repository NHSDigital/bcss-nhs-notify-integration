from services.NHSNotify import NHSNotify
from services.AuthManager import AuthManager
from services.DataAccess import DataAccess


class TestBCSSCommsManager:

    ### In here probably want to catch things like missing recipients and routing config id since this is their first point of entry

    def setup_method(
        self,
        method,
        nhs_notify_base_url,
        document_db_uri,
        document_db_name,
        document_db_collection,
    ):
        print(f"Setting up test {method}")
        self.nhs_notify = NHSNotify(nhs_notify_base_url)
        self.auth_manager: AuthManager = AuthManager()
        self.data_access = DataAccess(
            document_db_uri,
            document_db_name,
            document_db_collection,
        )

    def teardown_method(self, method):
        print(f"Tearing down test {method}")

    def test_initialization(
        self,
        nhs_notify_base_url,
        document_db_uri,
        document_db_name,
        document_db_collection,
    ):
        assert self.nhs_notify.api_client.base_url == nhs_notify_base_url
        assert self.data_access.collection_name == document_db_collection
        assert self.data_access.db_handler.client == document_db_uri
        assert self.data_access.db_handler.db.name == document_db_name

    def test_send_pre_invitation_single(self):
        # recipients length = 1
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

    def test_send_pre_invitation_single_missing_routing_config(self):
        # recipients length = 1
        # no routing config id
        # Mock the auth manager for an access token
        # Mock the notify and data access
        pass

    def test_send_pre_invitation_batch(self):
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

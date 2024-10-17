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

    def test_initialization(self, nhs_notify_base_url):
        assert self.nhs_notify.api_client.base_url == nhs_notify_base_url
        pass

    def test_send_single_message(self):
        self.nhs_notify.send_single_message
        # Correct setup correct access token, mock correct request body
        # Mock request
        pass

    def test_send_single_message_fail_access_token(self):
        # Incorrect/missing access token
        # Mock request
        pass

    def test_send_single_message_fail_request_body(self):
        # Incorrect/missing request body
        # Mock request
        pass

    def test_send_batch_message(self):
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

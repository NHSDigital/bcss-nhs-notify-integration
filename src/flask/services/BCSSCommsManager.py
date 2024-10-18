from .NHSNotify import NHSNotify
from .AuthManager import AuthManager
from .DataAccess import DataAccess

import os


class BCSSCommsManager:

    def __init__(self):
        self.nhs_notify: NHSNotify = NHSNotify(os.getenv("NHS_NOTIFY_BASE_URL"))
        self.auth_manager: AuthManager = AuthManager()
        self.data_access = DataAccess(
            os.getenv("DOCUMENT_DB_URI"),
            os.getenv("DOCUMENT_DB_NAME"),
            os.getenv("DOCUMENT_DB_COLLECTION"),
        )

    def send_pre_inviation(self, routing_config_id: str, recipients: list[str]) -> dict:
        access_token: str = self.auth_manager.get_access_token()

        if len(recipients) == 1:
            single_message_response = self.nhs_notify.send_single_message(
                access_token, routing_config_id, recipients[0]
            )
            self.data_access.create_data(data=single_message_response)
            return single_message_response
        else:
            batch_message_response = self.nhs_notify.send_batch_message(
                access_token, routing_config_id, recipients
            )
            self.data_access.create_data(data=batch_message_response)
            return batch_message_response

    def get_message_status(self, message_id: str) -> dict:
        access_token: str = self.auth_manager.get_access_token()
        response = self.nhs_notify.get_message_status(access_token, message_id)
        return response

    def get_nhs_app_account_details(self, ods_code: str, page_number: str):
        access_token: str = self.auth_manager.get_access_token()
        response = self.nhs_notify.get_NHS_acccount_details(
            access_token, ods_code, page_number
        )
        return response

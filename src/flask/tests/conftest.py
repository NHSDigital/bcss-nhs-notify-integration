import pytest
import json
import uuid
import os
from time import time
from services.base_api_client import BaseAPIClient
from services.nhs_notify import NHSNotify
from services.bcss_comms_manager import BCSSCommsManager
from services.auth_manager import AuthManager
from services.data_access import DataAccess

## FIXTURE CATEGORIES

#### LOCAL ENV FIXTURES
#### CLASS FIXTURES
#### API FIXTURES
#### MESSAGE FIXTURES
#### AUTH FIXTURES
#### UTIL MOCK RESPONSES
#### SUCCESSFUL API CALL MOCK RESPONSES
#### ERROR RESPONSES FROM NOTIFY


#### LOCAL ENV FIXTURES ####


@pytest.fixture()
def routing_config_id() -> str:
    return os.getenv("ROUTING_PLAN_ID")


@pytest.fixture()
def nhs_notify_base_url():
    yield os.getenv("NHS_NOTIFY_BASE_URL")


@pytest.fixture()
def api_key() -> str:
    return os.getenv("API_KEY")


@pytest.fixture()
def token_url() -> str:
    return os.getenv("TOKEN_URL")


@pytest.fixture()
def kid() -> str:
    return os.getenv("KID")


@pytest.fixture()
def private_key_path() -> str:
    return os.getenv("PRIVATE_KEY_PATH")


@pytest.fixture()
def document_db_uri() -> str:
    return os.getenv("DOCUMENT_DB_URI")


@pytest.fixture()
def document_db_name() -> str:
    return os.getenv("DOCUMENT_DB_NAME")


@pytest.fixture()
def document_db_collection() -> str:
    return os.getenv("DOCUMENT_DB_COLLECTION")


@pytest.fixture()
def generic_api_url() -> str:
    return "https://reqres.in"


@pytest.fixture()
def test_routing_config_id() -> str:
    return "test_routing_config_id"


@pytest.fixture()
def test_message_id() -> str:
    return "test_message_id"


@pytest.fixture()
def test_access_token() -> str:
    return "test_access_token"


@pytest.fixture()
def test_ODS_code() -> str:
    return "T00001"


@pytest.fixture()
def test_jwt() -> str:
    return "test_jwt"


#### CLASS FIXTURES ####


@pytest.fixture()
def auth_manager():
    temp_auth_manager = AuthManager()
    yield temp_auth_manager


@pytest.fixture()
def base_api_client_token(token_url) -> BaseAPIClient:
    return BaseAPIClient(token_url)


@pytest.fixture()
def base_api_client_notify(nhs_notify_base_url):
    yield BaseAPIClient(nhs_notify_base_url)


@pytest.fixture()
def bcss_comms_manager(nhs_notify, auth_manager, data_access):
    temp_bcss_comms_manager = BCSSCommsManager()
    temp_bcss_comms_manager.nhs_notify = nhs_notify
    temp_bcss_comms_manager.auth_manager = auth_manager
    temp_bcss_comms_manager.data_access = data_access
    yield temp_bcss_comms_manager


@pytest.fixture()
def data_access(document_db_uri, document_db_name, document_db_collection):
    temp_data_access = DataAccess(
        document_db_uri, document_db_name, document_db_collection
    )
    yield temp_data_access


@pytest.fixture()
def generic_base_api_client(generic_api_url):
    temp_generic_base_api_client = BaseAPIClient(generic_api_url)
    yield temp_generic_base_api_client


@pytest.fixture()
def nhs_notify(nhs_notify_base_url):
    temp_nhs_notify = NHSNotify(nhs_notify_base_url)
    yield temp_nhs_notify


#### API FIXTURES ####


@pytest.fixture()
def request_headers() -> dict:
    return {
        "content-type": "application/vnd.api+json",
        "accept": "application/vnd.api+json",
        "x-correlation-id": str(uuid.uuid4()),
    }


@pytest.fixture()
def request_body() -> json:
    return {
        "data": {
            "type": "Message",
            "attributes": {
                "messageReference": str(uuid.uuid4()),
                "recipient": {"nhsNumber": "9990548609", "dateOfBirth": "1932-01-06"},
                "originator": {"odsCode": "X26"},
                "personalisation": {"custom": "value"},
            },
        }
    }


#### MESSAGE FIXTURES #####


@pytest.fixture()
def test_recipient() -> dict:
    return {
        "NHS#": "9990548609",
        "dob": "1932-01-06",
    }


@pytest.fixture()
def test_recipient_missing_nhs_number() -> dict:
    return {
        "NHS#": "",
        "dob": "1932-01-06",
    }


@pytest.fixture()
def test_recipient_missing_dob() -> dict:
    return {
        "NHS#": "9990548609",
        "dob": "",
    }


@pytest.fixture()
def test_recipient_batch() -> dict:
    return ["9990548609", "9800100369"]


@pytest.fixture()
def test_notify_message_base() -> json:
    return {
        "messageReference": str(uuid.uuid4()),
        "recipient": {
            "nhsNumber": "9990548609",
            "dateOfBirth": "1932-01-06",
        },
        "originator": {"odsCode": "X26"},
        "personalisation": {"custom": "value"},
    }


#### AUTH FIXTURES ####


@pytest.fixture()
def test_jwt_params(api_key, token_url) -> dict:
    return {
        "algorithm": "RS512",
        "expiry_minutes": 5,
        "headers": {"alg": "RS512", "typ": "JWT", "kid": "test-kid"},
        "payload": {
            "sub": api_key,
            "iss": api_key,
            "jti": str(uuid.uuid4()),
            "aud": token_url,
            "exp": int(time()) + 300,
        },
    }


@pytest.fixture()
def test_get_access_token_mock_response(test_access_token) -> json:
    return {
        "access_token": test_access_token,
        "expires_in": "599",
        "token_type": "Bearer",
        "issued_at": "1729513788811",
    }


@pytest.fixture()
def get_access_token_failed_jwt_response() -> json:
    return {
        "error": "invalid_request",
        "error_description": "Malformed JWT in client_assertion",
        "message_id": "rrt-4354921348896248477-c-geu2-2703741-1330684-1",
    }


#### UTIL MOCK RESPONSES ####


@pytest.fixture()
def generate_notify_single_mock_response(test_routing_config_id) -> json:
    return {
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": test_routing_config_id,
                "messageReference": "test_message_reference",
                "recipient": {"nhsNumber": "9990548609", "dateOfBirth": "1932-01-06"},
                "originator": {"odsCode": "X26"},
                "personalisation": {"custom": "value"},
            },
        }
    }


@pytest.fixture()
def generate_notify_batch_mock_response(test_routing_config_id) -> json:
    return {
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": test_routing_config_id,
                "messageBatchReference": "test_message_batch_reference",
                "messages": [
                    {
                        "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "1932-01-06",
                        },
                        "originator": {"odsCode": "X26"},
                        "personalisation": {"custom": "value"},
                    }
                ],
            },
        }
    }


#### SUCCESSFUL API CALL MOCK RESPONSES ####


@pytest.fixture()
def single_message_request_mock_response(test_routing_config_id) -> json:
    return {
        "data": {
            "attributes": {
                "messageReference": "e69744f8-d288-4e27-b5fb-25c7c6f8cb14",
                "messageStatus": "created",
                "routingPlan": {
                    "version": "oCvakVm0FA_z3Z1H6C5ekHGffqYaqVCs",
                    "id": test_routing_config_id,
                },
                "timestamps": {"created": "2024-10-02T14:38:11.278Z"},
            },
            "links": {
                "self": "https://int.api.service.nhs.uk/comms/v1/messages/2msz6DlaaPNar5X6MwWHtbegAaV"
            },
            "id": "2msz6DlaaPNar5X6MwWHtbegAaV",
            "type": "Message",
        }
    }


@pytest.fixture()
def batch_message_request_mock_response(test_routing_config_id) -> json:
    return {
        "data": {
            "type": "MessageBatch",
            "id": "2mpxCN9i0yXQY9ZnL6uwC85Nr6x",
            "attributes": {
                "messageBatchReference": "0e8a0d1d-5fa3-4bfd-ac9f-9c3229411574",
                "routingPlan": {
                    "id": test_routing_config_id,
                    "version": "oCvakVm0FA_z3Z1H6C5ekHGffqYaqVCs",
                },
            },
        }
    }


@pytest.fixture()
def notify_get_message_status_response(test_message_id, test_routing_config_id) -> json:
    return {
        "data": {
            "type": "Message",
            "id": test_message_id,
            "attributes": {
                "messageReference": "063cee1b-2740-422d-b90d-d6ca34da44d5",
                "messageStatus": "pending_enrichment",
                "timestamps": {"created": "2024-10-18T15:12:44.986Z"},
                "routingPlan": {
                    "id": test_routing_config_id,
                    "version": "oCvakVm0FA_z3Z1H6C5ekHGffqYaqVCs",
                },
            },
            "links": {
                "self": "https://int.api.service.nhs.uk/comms/v1/messages/2ncFGwT2zNEk9KFFjEivGlFPZMZ"
            },
        }
    }


@pytest.fixture()
def notify_get_nhs_app_account_details_mock_response() -> json:
    return {
        "data": {
            "type": "NhsAppAccounts",
            "id": "T00001",
            "attributes": {
                "accounts": [
                    {"nhsNumber": "9303411455", "notificationsEnabled": True},
                    {"nhsNumber": "9684099843", "notificationsEnabled": False},
                ]
            },
        },
        "links": {
            "last": "https://int.api.service.nhs.uk/comms/channels/nhsapp/accounts?ods-organisation-code=T00001&page=5",
            "self": "https://int.api.service.nhs.uk/comms/channels/nhsapp/accounts?ods-organisation-code=T00001&page=2",
            "next": "https://int.api.service.nhs.uk/comms/channels/nhsapp/accounts?ods-organisation-code=T00001&page=3",
        },
    }


@pytest.fixture()
def test_generic_api_response() -> json:
    return {
        "page": 1,
        "per_page": 6,
        "total": 12,
        "total_pages": 2,
        "data": [
            {
                "id": 1,
                "email": "george.bluth@reqres.in",
                "first_name": "George",
                "last_name": "Bluth",
                "avatar": "https://reqres.in/img/faces/1-image.jpg",
            },
            {
                "id": 2,
                "email": "janet.weaver@reqres.in",
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://reqres.in/img/faces/2-image.jpg",
            },
            {
                "id": 3,
                "email": "emma.wong@reqres.in",
                "first_name": "Emma",
                "last_name": "Wong",
                "avatar": "https://reqres.in/img/faces/3-image.jpg",
            },
            {
                "id": 4,
                "email": "eve.holt@reqres.in",
                "first_name": "Eve",
                "last_name": "Holt",
                "avatar": "https://reqres.in/img/faces/4-image.jpg",
            },
            {
                "id": 5,
                "email": "charles.morris@reqres.in",
                "first_name": "Charles",
                "last_name": "Morris",
                "avatar": "https://reqres.in/img/faces/5-image.jpg",
            },
            {
                "id": 6,
                "email": "tracey.ramos@reqres.in",
                "first_name": "Tracey",
                "last_name": "Ramos",
                "avatar": "https://reqres.in/img/faces/6-image.jpg",
            },
        ],
        "support": {
            "url": "https://reqres.in/#support-heading",
            "text": "To keep ReqRes free, contributions towards server costs are appreciated!",
        },
    }


#### ERROR RESPONSES FROM NOTIFY ####


@pytest.fixture()
def notify_401_missing_auth_request_mock_response() -> json:
    return {
        "errors": [
            {
                "id": "rrt-1931948104716186917-c-geu2-10664-3111479-3.0",
                "code": "CM_DENIED",
                "links": {
                    "about": "https://digital.nhs.uk/developer/api-catalogue/nhs-notify"
                },
                "status": "401",
                "title": "Access denied",
                "detail": "Access token missing, invalid or expired, or calling application not configured for this operation.",
                "source": {"header": "Authorization"},
            }
        ]
    }


@pytest.fixture()
def notify_400_missing_nhs_number_mock_response() -> json:
    return {
        "errors": [
            {
                "id": "rrt-2709357079573522931-b-geu2-1562214-7061178-2.0",
                "code": "CM_INVALID_NHS_NUMBER",
                "links": {
                    "about": "https://digital.nhs.uk/developer/api-catalogue/nhs-notify",
                    "nhsNumbers": "https://www.datadictionary.nhs.uk/attributes/nhs_number.html",
                },
                "status": "400",
                "title": "Invalid nhs number",
                "detail": "The value provided in this nhsNumber field is not a valid NHS number.",
                "source": {"pointer": "/data/attributes/recipient/nhsNumber"},
            }
        ]
    }


@pytest.fixture()
def notify_400_incorrect_routing_config_request_mock_response() -> json:
    return {
        "errors": [
            {
                "id": "rrt-347680715282487770-c-geu2-1809628-6172494-2.0",
                "code": "CM_INVALID_VALUE",
                "links": {
                    "about": "https://digital.nhs.uk/developer/api-catalogue/nhs-notify"
                },
                "status": "400",
                "title": "Invalid value",
                "detail": "The property at the specified location does not allow this value.",
                "source": {"pointer": "/data/attributes/routingPlanId"},
            }
        ]
    }


@pytest.fixture()
def notify_400_missing_dob_mock_response() -> json:
    return {
        "errors": [
            {
                "id": "rrt-48133796090514339-a-geu2-2913303-6913317-2.1",
                "code": "CM_INVALID_VALUE",
                "links": {
                    "about": "https://digital.nhs.uk/developer/api-catalogue/nhs-notify"
                },
                "status": "400",
                "title": "Invalid value",
                "detail": "The property at the specified location does not allow this value.",
                "source": {"pointer": "/data/attributes/recipient/dateOfBirth"},
            }
        ]
    }


# What is currently returned if making a get message status call with no ID (Postman)
@pytest.fixture()
def notify_403_forbidden_response() -> json:
    return {
        "errors": [
            {
                "id": "rrt-1299718902873520380-b-geu2-375102-2184555-2.0",
                "code": "CM_FORBIDDEN",
                "links": {
                    "about": "https://digital.nhs.uk/developer/api-catalogue/nhs-notify"
                },
                "status": "403",
                "title": "Forbidden",
                "detail": "Client not recognised or not yet onboarded.",
                "source": {"header": "Authorization"},
            }
        ]
    }


@pytest.fixture()
def notify_400_missing_ods_code_response() -> json:
    return {
        "errors": [
            {
                "id": "rrt-4354921348896248477-c-geu2-2703740-1217381-2.0",
                "code": "CM_INVALID_REQUEST",
                "links": {
                    "about": "https://digital.nhs.uk/developer/api-catalogue/nhs-notify"
                },
                "status": "400",
                "title": "Invalid Request",
                "detail": "Missing ODS Code",
            }
        ]
    }

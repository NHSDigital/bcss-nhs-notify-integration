import pytest
import json
import uuid
from dotenv import dotenv_values
from time import time
from services.BaseAPIClient import BaseAPIClient

config = dotenv_values("../.env")

#### LOCAL ENV FIXTURES ####


@pytest.fixture()
def routing_config_id() -> str:
    return config.get("ROUTING_PLAN_ID")


@pytest.fixture()
def nhs_notify_base_url() -> str:
    return config.get("NHS_NOTIFY_BASE_URL")


@pytest.fixture()
def api_key() -> str:
    return config.get("API_KEY")


@pytest.fixture()
def token_url() -> str:
    return config.get("TOKEN_URL")


@pytest.fixture()
def kid() -> str:
    return config.get("KID")


@pytest.fixture()
def private_key_path() -> str:
    return config.get("PRIVATE_KEY_PATH")


#### CLASS FIXTURES ####


@pytest.fixture()
def base_api_client_token(token_url) -> BaseAPIClient:
    return BaseAPIClient(token_url)


@pytest.fixture()
def base_api_client_notify(nhs_notify_base_url) -> BaseAPIClient:
    return BaseAPIClient(nhs_notify_base_url)


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
def test_recipient_batch() -> dict:
    return [
        {"NHS#": "9990548609", "dob": "1932-01-06"},
        {"NHS#": "9800100369", "dob": "1983-12-03"},
    ]


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
def test_jwt_params(kid, api_key, token_url) -> dict:
    return {
        "algorithm": "RS512",
        "expiry_minutes": 5,
        "headers": {"alg": "RS512", "typ": "JWT", "kid": kid},
        "payload": {
            "sub": api_key,
            "iss": api_key,
            "jti": str(uuid.uuid4()),
            "aud": token_url,
            "exp": int(time()) + 300,
        },
    }


#### UTIL MOCK RESPONSES ####


@pytest.fixture()
def generate_notify_single_mock_response() -> json:
    return {
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "test_routing_config_id",
                "messageReference": "test_message_reference",
                "recipient": {"nhsNumber": "9990548609", "dateOfBirth": "1932-01-06"},
                "originator": {"odsCode": "X26"},
                "personalisation": {"custom": "value"},
            },
        }
    }


@pytest.fixture()
def generate_notify_batch_mock_response() -> json:
    return {
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "test_routing_config_id",
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


#### API CALL MOCK RESPONSES ####


@pytest.fixture()
def single_message_request_mock_response() -> json:
    return {
        "data": {
            "attributes": {
                "messageReference": "e69744f8-d288-4e27-b5fb-25c7c6f8cb14",
                "messageStatus": "created",
                "routingPlan": {
                    "version": "oCvakVm0FA_z3Z1H6C5ekHGffqYaqVCs",
                    "id": "test_routing_config_id",
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
def batch_message_request_mock_response() -> json:
    return {
        "data": {
            "type": "MessageBatch",
            "id": "2mpxCN9i0yXQY9ZnL6uwC85Nr6x",
            "attributes": {
                "messageBatchReference": "0e8a0d1d-5fa3-4bfd-ac9f-9c3229411574",
                "routingPlan": {
                    "id": "test_routing_config_id",
                    "version": "oCvakVm0FA_z3Z1H6C5ekHGffqYaqVCs",
                },
            },
        }
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

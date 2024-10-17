import pytest
import json
import uuid
from dotenv import dotenv_values
from time import time

config = dotenv_values("../.env")


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


@pytest.fixture()
def test_recipient() -> dict:
    return {
        "NHS#": "9990548609",
        "dob": "1932-01-06",
    }


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


@pytest.fixture()
def test_notify_message_single() -> json:
    return {
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": "test_routing_config_id",
                "messageReference": str(uuid.uuid4()),
                "recipient": {"nhsNumber": "9990548609", "dateOfBirth": "1932-01-06"},
                "originator": {"odsCode": "X26"},
                "personalisation": {"custom": "value"},
            },
        }
    }


@pytest.fixture()
def test_notify_message_batch() -> json:
    return {
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "test_routing_config_id",
                "messageBatchReference": "test_message_batch_reference",
                "messages": list(map(Util.generate_message, recipients)),
            },
        }
    }


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

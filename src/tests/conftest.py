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

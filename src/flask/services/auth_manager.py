import json
from time import time
import uuid
from dotenv import dotenv_values
import os

from .base_api_client import BaseAPIClient
from .util import Util

config = dotenv_values("../.env")


class AuthManager:
    def __init__(self) -> None:
        self.api_client: BaseAPIClient = BaseAPIClient(config.get("TOKEN_URL"))

    def get_access_token(self) -> str:

        jwt: str = self.generate_auth_jwt()

        headers: dict = {"Content-Type": "application/x-www-form-urlencoded"}

        body = {
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": jwt,
        }

        response = self.api_client.make_request(
            "POST", "", data=body, headers=headers, params=None
        )
        responseJson = response.json()
        access_token = responseJson["access_token"]

        return access_token

    def generate_auth_jwt(self) -> str:
        algorithm: str = "RS512"

        expiry_minutes: int = 5

        headers: dict = {"alg": algorithm, "typ": "JWT", "kid": config.get("KID")}

        payload: dict = {
            "sub": config.get("API_KEY"),
            "iss": config.get("API_KEY"),
            "jti": str(uuid.uuid4()),
            "aud": config.get("TOKEN_URL"),
            "exp": int(time()) + 300,  # 5mins in the future
        }

        private_key = Util.get_private_key(config.get("PRIVATE_KEY_PATH"))

        return Util.generate_jwt(
            algorithm, private_key, headers, payload, expiry_minutes=5
        )

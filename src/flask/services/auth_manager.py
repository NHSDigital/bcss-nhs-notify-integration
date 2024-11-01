from time import time
import uuid
import os

from .base_api_client import BaseAPIClient
from .util import Util


class AuthManager:
    def __init__(self) -> None:
        self.api_client: BaseAPIClient = BaseAPIClient(os.getenv("TOKEN_URL"))

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
        access_token = response["access_token"]

        return access_token

    def generate_auth_jwt(self) -> str:
        algorithm: str = "RS512"

        expiry_minutes: int = 5

        headers: dict = {"alg": algorithm, "typ": "JWT", "kid": os.getenv("KID")}

        payload: dict = {
            "sub": os.getenv("API_KEY"),
            "iss": os.getenv("API_KEY"),
            "jti": str(uuid.uuid4()),
            "aud": os.getenv("TOKEN_URL"),
            "exp": int(time()) + 300,  # 5mins in the future
        }

        private_key = Util.get_private_key(os.getenv("PRIVATE_KEY_PATH"))

        return Util.generate_jwt(
            algorithm, private_key, headers, payload, expiry_minutes
        )

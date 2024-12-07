import requests

from goodhomepy.models import *

# Client
class GoodHomeClient:
    BASE_URL = "https://shkf02.goodhome.com"

    def __init__(self, token: str = None):
        self.token = token

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, email: str, password: str) -> AuthResponse:
        url = f"{self.BASE_URL}/v1/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(url, json=payload, headers=self._get_headers())
        response.raise_for_status()
        auth_response = AuthResponse(**response.json())
        self.token = auth_response.token
        return auth_response

    def refresh_token(self, refresh_token: str) -> RefreshTokenResponse:
        url = f"{self.BASE_URL}/v1/auth/token"
        params = {
            "refresh_token": refresh_token
        }
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return RefreshTokenResponse(**response.json())

    def verify_token(self, token: str) -> VerifyTokenResponse:
        url = f"{self.BASE_URL}/v1/auth/verify"
        params = {
            "token": token
        }
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return VerifyTokenResponse(**response.json())

    def get_devices(self, user_id: str) -> List[Device]:
        url = f"{self.BASE_URL}/v1/users/{user_id}/devices"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        devices = response.json().get("devices", [])
        return [Device(**item) for item in devices]

    def get_user(self, user_id: str) -> User:
        url = f"{self.BASE_URL}/v1/users/{user_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return User(**response.json())

    def get_homes(self, user_id: str) -> List[str]:
        url = f"{self.BASE_URL}/v1/users/{user_id}/homes"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        homes = response.json().get("homes", [])
        return [Home(**item) for item in homes]

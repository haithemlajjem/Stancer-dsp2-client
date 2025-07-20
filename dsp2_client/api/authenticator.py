import httpx

from .. import config, logger


class DSP2Authenticator:
    """
    Handles DSP2 authentication, token retrieval, and storage.
    """

    def __init__(self, username: str, password: str, client: httpx.Client):
        if not username or not password:
            raise ValueError("Username and password must be provided")
        self.username = username
        self.password = password
        self.client = client
        self.token: str | None = None

    def authenticate(self) -> str:
        """
        Authenticate with DSP2 API and store the token.
        """
        token_url = config.TOKEN_ENDPOINT
        payload = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": "stet",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = self.client.post(token_url, data=payload, headers=headers)
            response.raise_for_status()

            token_data = response.json()
            self.token = token_data.get("access_token")

            if not self.token:
                raise RuntimeError("Failed to obtain access token")

            logger.logger.info("Authentication successful")
            return self.token
        except httpx.HTTPStatusError as e:
            logger.logger.error(f"HTTP error during authentication: {e.response.text}")
            raise RuntimeError("Authentication failed") from e
        except Exception as e:
            logger.logger.error(f"Unexpected error during authentication: {e}")
            raise RuntimeError("Authentication failed") from e

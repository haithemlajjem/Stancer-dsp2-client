import httpx

from .. import logger


class BaseAPIClient:
    """
    A base HTTP client for GET and POST requests with error handling.
    """

    def __init__(self, base_url: str, token: str | None = None):
        self._client = httpx.Client(base_url=str(base_url))
        if token:
            self._client.headers.update({"Authorization": f"Bearer {token}"})

    def set_token(self, token: str):
        """Update the Authorization header with a new token."""
        self._client.headers.update({"Authorization": f"Bearer {token}"})

    def get(self, endpoint: str, params: dict | None = None) -> dict:
        try:
            logger.logger.debug(f"GET {endpoint} with params={params}")
            response = self._client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.logger.error(f"HTTP error on GET {endpoint}: {e.response.text}")
            raise RuntimeError(f"Failed GET {endpoint}") from e
        except Exception as e:
            logger.logger.error(f"Unexpected error on GET {endpoint}: {e}")
            raise RuntimeError(f"Failed GET {endpoint}") from e

from unittest.mock import MagicMock, patch

import pytest

from dsp2_client.api.api_client import DSP2Client


@pytest.fixture
def valid_user_identity():
    return {
        "id": "user_TLMLiOYdrPdO7YYuuLdK9Dvw",
        "prefix": "DOCT",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
    }


@pytest.fixture
def valid_account():
    return {
        "id": "acct_x05RAIZbtzKCUJ7m1MEnzOI5",
        "type": "CACC",
        "usage": "PRIV",
        "iban": "IBAN12345678901234",
        "name": "Test Account",
        "currency": "EUR",
    }


@pytest.fixture
def authenticated_client():
    with patch("httpx.Client.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "token123"}
        mock_post.return_value = mock_response
        yield DSP2Client("user", "pass")

from unittest.mock import MagicMock, patch

import pytest

from dsp2_client.api_client import DSP2Client
from dsp2_client.models import AccountSchema, UserIdentitySchema


@pytest.fixture
def client():
    """
    Fixture that returns a DSP2Client instance with mocked token authentication.
    """
    with patch("httpx.Client.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"access_token": "token123"}
        mock_post.return_value = mock_response
        yield DSP2Client("user", "pass")


def test_get_identity(client):
    """
    Ensure get_identity returns expected UserIdentitySchema object.
    """
    mock_data = {
        "id": "user_xjRTE0pozug4jZ7RId2H8rWZ",
        "prefix": "DOCT",
        "first_name": "Alice",
        "last_name": "Bob",
        "date_of_birth": "2000-01-01",
    }

    with patch.object(client._client, "get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = mock_data

        identity = client.get_identity()
        assert isinstance(identity, UserIdentitySchema)
        assert identity.id == mock_data["id"]
        assert identity.first_name == mock_data["first_name"]
        assert identity.last_name == mock_data["last_name"]


def test_get_accounts(client):
    """
    Ensure get_accounts returns list of AccountSchema with valid data.
    """
    mock_data = [
        {
            "id": "acct_123",
            "type": "CACC",
            "usage": "PRIV",
            "iban": "DE123456789",
            "name": "Main Account",
            "currency": "EUR",
        }
    ]

    with patch.object(client._client, "get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = mock_data

        accounts = client.get_accounts()
        assert isinstance(accounts, list)
        assert all(isinstance(acc, AccountSchema) for acc in accounts)
        assert accounts[0].id == mock_data[0]["id"]
        assert accounts[0].currency == "EUR"


def test_get_accounts_empty_list(client):
    """
    Ensure get_accounts handles empty response.
    """
    with patch.object(client._client, "get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = []

        accounts = client.get_accounts()
        assert isinstance(accounts, list)
        assert accounts == []


def test_get_method_raises_runtime_error_on_http_error(client):
    """
    Ensure RuntimeError is raised on HTTP failure inside _get.
    """
    with patch.object(client._client, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP failure")
        mock_get.return_value = mock_response

        with pytest.raises(RuntimeError, match="Failed GET"):
            client._get("/failing-endpoint")

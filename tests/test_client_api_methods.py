from unittest.mock import patch

import pytest

from dsp2_client.models.account import AccountSchema
from dsp2_client.models.identity import UserIdentitySchema


def test_get_identity(authenticated_client, valid_user_identity):
    with patch.object(authenticated_client.api._client, "get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = valid_user_identity

        identity = authenticated_client.get_identity()
        assert isinstance(identity, UserIdentitySchema)
        assert identity.id == valid_user_identity["id"]
        assert identity.first_name == valid_user_identity["first_name"]


def test_get_accounts(authenticated_client, valid_account):
    with patch.object(authenticated_client.api._client, "get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = [valid_account]

        accounts = authenticated_client.get_accounts()
        assert isinstance(accounts, list)
        assert all(isinstance(acc, AccountSchema) for acc in accounts)
        assert accounts[0].id == valid_account["id"]


def test_get_accounts_empty_list(authenticated_client):
    with patch.object(authenticated_client.api._client, "get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = []

        accounts = authenticated_client.get_accounts()
        assert accounts == []


def test_get_method_raises_runtime_error_on_http_error(authenticated_client):
    with patch.object(authenticated_client.api._client, "get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.raise_for_status.side_effect = Exception("HTTP failure")

        with pytest.raises(RuntimeError, match="Failed GET"):
            authenticated_client.api.get("/failing-endpoint")

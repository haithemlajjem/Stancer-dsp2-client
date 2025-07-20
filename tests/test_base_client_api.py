from unittest.mock import MagicMock, patch

import pytest

from dsp2_client.api.base_client import BaseAPIClient


@pytest.fixture
def client():
    """Fixture to create a BaseAPIClient instance for tests."""
    return BaseAPIClient("http://api.test")


@pytest.fixture
def mock_response():
    """Fixture for a reusable mock HTTP response."""
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"result": "ok"}
    return response


@patch("httpx.Client.get")
def test_get_success(mock_get, client, mock_response):
    """Test successful GET request."""
    mock_get.return_value = mock_response
    response = client.get("/test")
    assert response == {"result": "ok"}


@patch("httpx.Client.get")
@pytest.mark.parametrize("error_message", ["Error", "Some HTTP failure"])
def test_get_http_error(mock_get, client, error_message):
    """Test GET request that raises HTTP error."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception(error_message)
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="Failed GET"):
        client.get("/fail")


def test_set_token(client):
    """Test setting the authorization token."""
    client.set_token("abc123")
    assert client._client.headers["Authorization"] == "Bearer abc123"


def test_set_token_overwrites(client):
    """Ensure token is overwritten when set again."""
    client.set_token("abc123")
    client.set_token("newtoken")
    assert client._client.headers["Authorization"] == "Bearer newtoken"

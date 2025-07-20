from unittest.mock import MagicMock, patch

import pytest

from dsp2_client.api.api_client import DSP2Client


@pytest.fixture
def mock_post():
    with patch("httpx.Client.post") as mock:
        yield mock


def test_authenticate_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "token123"}
    mock_post.return_value = mock_response

    client = DSP2Client("user", "pass")

    assert client.authenticator.token == "token123"
    assert client.api._client.headers["Authorization"] == "Bearer token123"


@pytest.mark.parametrize("status_code", [400, 401, 403, 500])
def test_authenticate_failure(mock_post, status_code):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.raise_for_status.side_effect = Exception("Bad request")
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="Authentication failed"):
        DSP2Client("user", "pass")


def test_authenticate_missing_access_token(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError):
        DSP2Client("user", "pass")


@pytest.mark.parametrize("username, password", [("", "pass"), ("user", ""), ("", "")])
def test_authenticate_missing_credentials(username, password):
    with pytest.raises(ValueError):
        DSP2Client(username, password)

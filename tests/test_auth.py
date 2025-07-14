from unittest.mock import MagicMock, patch

import pytest

from dsp2_client.api_client import DSP2Client


def test_authenticate_success():
    """
    Test that DSP2Client authenticates successfully when the API returns a 200 status code
    and provides an access token.
    """
    with patch("httpx.Client.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "token123"}
        mock_post.return_value = mock_response

        client = DSP2Client("user", "pass")
        assert client._token == "token123"
        assert "Authorization" in client._client.headers


def test_authenticate_failure():
    """
    Test that DSP2Client raises a RuntimeError when authentication fails.
    """
    with patch("httpx.Client.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = Exception("Bad request")
        mock_post.return_value = mock_response

        with pytest.raises(RuntimeError):
            DSP2Client("user", "pass")
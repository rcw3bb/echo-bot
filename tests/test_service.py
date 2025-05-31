"""
Unit tests for the service module in echo_bot.

Author: Ron Webb
Since: 1.0.0
"""

import pytest
from unittest.mock import patch, MagicMock
from echo_bot import service


def test_get_github_token_success(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "dummy-token")
    assert service.get_github_token() == "dummy-token"


def test_get_github_token_missing(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    # Patch load_dotenv to a no-op so .env is not loaded during this test
    with patch("echo_bot.service.load_dotenv", lambda: None):
        with pytest.raises(RuntimeError, match="GITHUB_TOKEN environment variable not set."):
            service.get_github_token()


def test_send_message_success(monkeypatch):
    dummy_response = {
        "choices": [
            {"message": {"content": "Hello from the assistant!"}}
        ]
    }
    mock_post = MagicMock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = dummy_response
    mock_post.return_value.raise_for_status = MagicMock()
    monkeypatch.setenv("GITHUB_TOKEN", "dummy-token")
    with patch("echo_bot.service.requests.post", mock_post):
        messages = [{"role": "user", "content": "Hi!"}]
        reply = service.send_message(messages)
        assert reply == "Hello from the assistant!"
        mock_post.assert_called_once()


def test_send_message_http_error(monkeypatch):
    mock_post = MagicMock()
    mock_post.return_value.raise_for_status.side_effect = Exception("HTTP error")
    monkeypatch.setenv("GITHUB_TOKEN", "dummy-token")
    with patch("echo_bot.service.requests.post", mock_post):
        messages = [{"role": "user", "content": "Hi!"}]
        with pytest.raises(Exception, match="HTTP error"):
            service.send_message(messages)

def test_send_message_payload(monkeypatch):
    """
    Test that send_message sends the correct payload and headers.
    """
    dummy_response = {
        "choices": [
            {"message": {"content": "Test payload!"}}
        ]
    }
    mock_post = MagicMock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = dummy_response
    mock_post.return_value.raise_for_status = MagicMock()
    monkeypatch.setenv("GITHUB_TOKEN", "dummy-token")
    with patch("echo_bot.service.requests.post", mock_post):
        messages = [{"role": "user", "content": "Payload?"}]
        service.send_message(messages)
        args, kwargs = mock_post.call_args
        assert args[0] == service.GITHUB_API_URL
        assert kwargs["headers"]["Authorization"] == "Bearer dummy-token"
        assert kwargs["headers"]["Content-Type"] == "application/json"
        assert kwargs["data"] is not None
        assert "model" in kwargs["data"]
        assert "messages" in kwargs["data"]
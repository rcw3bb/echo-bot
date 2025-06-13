"""
Test module for echo_bot.chatbot.

Author: Ron Webb
Since: 1.0.0
"""

import builtins
import types
from echo_bot import chatbot
from echo_bot import service

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("HTTP error")
    def json(self):
        return self._json


def test_send_message(monkeypatch):
    """
    Test send_message returns the assistant's reply from the API response.
    """
    def dummy_post(url, headers, data, timeout):
        assert url == service.GITHUB_API_URL
        return DummyResponse({
            "choices": [
                {"message": {"content": "Hello!", "role": "assistant"}}
            ]
        })
    monkeypatch.setattr(service, "requests", types.SimpleNamespace(post=dummy_post))
    monkeypatch.setattr(service, "get_github_token", lambda: "dummy-token")
    messages = [{"role": "user", "content": "Hi"}]
    reply = service.send_message(messages)
    assert reply == "Hello!"


def test_run_chatbot_exit(monkeypatch):
    """
    Test run_chatbot exits on 'exit' command.
    """
    inputs = iter(["exit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    # Patch send_message to avoid real API call
    monkeypatch.setattr(chatbot, "send_message", lambda messages: "bye")
    # Patch print to capture output
    output = []
    def fake_print(*args, **kwargs):
        output.append(" ".join(str(arg) for arg in args))
    monkeypatch.setattr(builtins, "print", fake_print)
    chatbot.run_chatbot()
    assert any("Goodbye!" in str(line) for line in output)

def test_run_chatbot_keyboard_interrupt(monkeypatch):
    """
    Test run_chatbot exits gracefully on KeyboardInterrupt.
    """
    def raise_keyboard_interrupt(_):
        raise KeyboardInterrupt()
    monkeypatch.setattr(builtins, "input", raise_keyboard_interrupt)
    monkeypatch.setattr(chatbot, "send_message", lambda messages: "bye")
    output = []
    def fake_print(*args, **kwargs):
        output.append(" ".join(str(arg) for arg in args))
    monkeypatch.setattr(builtins, "print", fake_print)
    chatbot.run_chatbot()
    assert any("Goodbye!" in str(line) for line in output)

def test_run_chatbot_empty_input(monkeypatch):
    """
    Test run_chatbot ignores empty input and continues loop.
    """
    inputs = iter(["", "exit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(chatbot, "send_message", lambda messages: "bye")
    output = []
    def fake_print(*args, **kwargs):
        output.append(" ".join(str(arg) for arg in args))
    monkeypatch.setattr(builtins, "print", fake_print)
    chatbot.run_chatbot()
    assert any("Goodbye!" in str(line) for line in output)

def test_run_chatbot_api_error(monkeypatch):
    """
    Test run_chatbot prints error if send_message raises exception.
    """
    inputs = iter(["fail", "exit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    def fail_send_message(messages):
        raise ValueError("API error")
    monkeypatch.setattr(chatbot, "send_message", fail_send_message)
    output = []
    def fake_print(*args, **kwargs):
        output.append(" ".join(str(arg) for arg in args))
    monkeypatch.setattr(builtins, "print", fake_print)
    chatbot.run_chatbot()
    assert any("[Error]" in str(line) for line in output)
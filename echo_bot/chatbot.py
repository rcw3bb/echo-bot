"""
Chatbot CLI module for echo_bot.

This module implements the command-line interface for interacting with the chatbot using the GitHub Inference API.
It handles user input, output formatting (including colored prompts and responses), and conversation flow.
All API communication is delegated to the service module.

Author: Ron Webb
Since: 1.0.0
"""

import requests
from . import __version__
from .service import send_message
from .util import setup_logger
from collections.abc import Sequence

logger = setup_logger(__name__)

SYSTEM_PROMPT = {"role": "system", "content": "You are Echo a helpful assistant."}


def _display_greeting() -> None:
    """
    Displays the welcome message.

    Author: Ron Webb
    Since: 1.1.0
    """
    header = f"Welcome to echo-bot v{__version__}! Type 'exit' to quit."
    print(header)
    logger.info(header)


def _display_goodbye() -> None:
    """
    Displays the goodbye message.

    Author: Ron Webb
    Since: 1.1.0
    """
    print("\n\033[35mGoodbye!\033[0m")
    logger.info("User exited the chatbot loop.")


def _handle_special_commands(user_input: str, messages: list[dict[str, str]]) -> bool:
    """
    Handles special commands like exit and reset. Returns True if the loop should continue, False to break.

    Author: Ron Webb
    Since: 1.1.0
    """
    if user_input.lower() in {"exit", "quit"}:
        _display_goodbye()
        logger.info("User requested exit command.")
        return False
    if user_input.lower() == "/reset":
        messages.clear()
        messages.append(SYSTEM_PROMPT.copy())
        logger.info("Conversation context reset by user.")
        return True
    return None


def _send_and_display_reply(messages: list[dict[str, str]]) -> None:
    """
    Sends the message to the service and displays the reply, handling errors.

    Author: Ron Webb
    Since: 1.1.0
    """
    try:
        reply = send_message(messages)
    except (requests.RequestException, ValueError, KeyError) as exc:
        logger.error("Error during send_message: %s", exc, exc_info=True)
        print(f"\033[31m[Error]\033[0m {exc}")
        return
    print(f"\033[36mEcho:\033[0m {reply}")
    messages.append({"role": "assistant", "content": reply})


def run_chatbot() -> None:
    """
    Runs the CLI chatbot loop.
    """
    _display_greeting()
    messages: list[dict[str, str]] = [SYSTEM_PROMPT.copy()]
    while True:
        try:
            user_input = input("\033[32m> \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            _display_goodbye()
            break
        if not user_input:
            continue
        special = _handle_special_commands(user_input, messages)
        if special is False:
            break
        if special is True:
            continue
        messages.append({"role": "user", "content": user_input})
        _send_and_display_reply(messages)

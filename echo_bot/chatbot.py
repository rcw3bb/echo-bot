"""
Chatbot CLI module for echo_bot.

This module implements the command-line interface for interacting with the chatbot using the GitHub Inference API.
It handles user input, output formatting (including colored prompts and responses), and conversation flow.
All API communication is delegated to the service module.

Author: Ron Webb
Since: 1.0.0
"""

import requests
from .service import send_message


def run_chatbot() -> None:
    """
    Runs the CLI chatbot loop.
    """
    print("Welcome to echo-bot v1.0.1! Type 'exit' to quit.")
    messages: list[dict[str, str]] = [
        {"role": "system", "content": "You are Echo a helpful assistant."}
    ]
    while True:
        try:
            user_input = input("\033[32m> \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\033[35mGoodbye!\033[0m")
            break
        if user_input.lower() in {"exit", "quit"}:
            print("\033[35mGoodbye!\033[0m")
            break
        if not user_input:
            continue
        messages.append({"role": "user", "content": user_input})
        try:
            reply = send_message(messages)
        except (requests.RequestException, ValueError, KeyError) as exc:
            print(f"\033[31m[Error]\033[0m {exc}")
            continue
        print(f"\033[36mEcho:\033[0m {reply}")
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "assistant", "content": reply})

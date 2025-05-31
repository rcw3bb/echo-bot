"""
Main entry point for echo_bot CLI chatbot.

Author: Ron Webb
Since: 1.0.0
"""

from .chatbot import run_chatbot


def main() -> None:
    """
    Entry point for the chatbot CLI.
    """
    run_chatbot()


if __name__ == "__main__":
    main()

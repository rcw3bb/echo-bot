"""
Service module for echo_bot. Handles communication with the GitHub Inference API.

Author: Ron Webb
Since: 1.0.0
"""

import os
import json
from collections.abc import Sequence
from typing import Any
from dotenv import load_dotenv
import requests
from .util import setup_logger

GITHUB_API_URL = "https://models.github.ai/inference/chat/completions"
MODEL_ID = "openai/gpt-4.1"

logger = setup_logger(__name__)


def get_github_token() -> str:
    """
    Retrieves the GitHub token from the environment variable GITHUB_TOKEN.
    Loads .env file if present.
    Raises an exception if not found.
    """
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logger.warning("GITHUB_TOKEN environment variable not set.")
        return None
    logger.debug("GITHUB_TOKEN successfully loaded.")
    return token


def send_message(messages: Sequence[dict[str, Any]]) -> str:
    """
    Sends a chat message to the GitHub Inference API and returns the assistant's reply.

    :param messages: The list of chat messages (role/content dicts).
    :return: The assistant's reply as a string.
    """
    token = get_github_token()
    if not token:
        logger.error("GITHUB_TOKEN is missing. Cannot send message.")
        return "Error: GITHUB_TOKEN environment variable not set. Please set it in your environment or .env file."
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_ID,
        "messages": messages,
    }
    logger.debug("Sending message to GitHub Inference API: %s", payload)
    try:
        response = requests.post(
            GITHUB_API_URL, headers=headers, data=json.dumps(payload), timeout=30
        )
        response.raise_for_status()
        data = response.json()
        logger.debug("Received response from API: %s", data)
        return data["choices"][0]["message"]["content"]
    except requests.RequestException as exc:
        logger.error("Request to GitHub Inference API failed: %s", exc, exc_info=True)
        raise
    except (KeyError, ValueError) as exc:
        logger.error("Error parsing API response: %s", exc, exc_info=True)
        raise

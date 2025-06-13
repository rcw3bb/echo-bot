"""
Logger utility module for echo_bot.

Author: Ron Webb
Since: 1.1.0
"""

import logging
import logging.config
import os


def setup_logger(name: str) -> logging.Logger:
    """
    Set up and return a logger configured using logging.ini.

    Args:
        name: The name of the logger.
    Returns:
        Configured logger instance.
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logging.ini")
    if os.path.exists(config_path):
        logging.config.fileConfig(config_path, disable_existing_loggers=False)
    return logging.getLogger(name)

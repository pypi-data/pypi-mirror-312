# basic_commands.py

import os
from cli_tool.config import LOGGER_CONFIG
from cli_logger.logger import setup_logger

logger = setup_logger(__name__, LOGGER_CONFIG)

def load():

    def clear(_):
        os.system('cls' if os.name == 'nt' else 'clear')

    return {
        "clear": clear
    }

# loader.py

import importlib.metadata
from cli_tool.config import LOGGER_CONFIG
from cli_logger.logger import setup_logger

logger = setup_logger(__name__, LOGGER_CONFIG)

def load_commands(commands):
    try:
        entry_points = importlib.metadata.entry_points(group="cli_tool.commands")
        for entry_point in entry_points:
            try:
                command_module = entry_point.load()
                logger.debug(f"Loaded module: {entry_point.name} -> {command_module}")

                if callable(command_module):
                    loaded_commands = command_module()
                    logger.debug(f"Loaded commands: {loaded_commands}")
                    commands.update(loaded_commands)
                else:
                    logger.warning(f"Entry point {entry_point.name} did not return a callable")
            except Exception as e:
                logger.error(f"Error loading command {entry_point.name}: {e}")
    except Exception as e:
        logger.error(f"Error discovering entry points: {e}")

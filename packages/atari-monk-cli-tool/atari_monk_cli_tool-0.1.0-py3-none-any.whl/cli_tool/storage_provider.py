import os
from cli_logger.logger import setup_logger
from cli_tool.config import LOGGER_CONFIG    
from pytoolbox.folder import ensure_folder_exists
from pytoolbox.json import save_json, load_json
from keyval_storage.storage import KeyValueStorage

logger = setup_logger(__name__, LOGGER_CONFIG)

STORAGE_FILE_PATH_KEY = 'cli_tool-key_value_file_path'
STORAGE_FILE_NAME = 'cli_tool-key_value.json'
CONFIG_FOLDER_PATH = 'C:\\cli_tool'
CONFIG_NAME = 'config.json'

class StorageProvider:
    def __init__(self):
        self._storage = None

    def initialize_storage(self):
        if not self._load_storage_file():
            self._create_storage_file()

    def _create_storage_file(self):
        try:
            data_folder_path = input("Provide PATH for cli_tool DATA FOLDER:> ").strip()
            ensure_folder_exists(data_folder_path)

            storage_file_path = os.path.join(data_folder_path, STORAGE_FILE_NAME)
            self._storage = KeyValueStorage(storage_file_path)
            self._storage.set(STORAGE_FILE_PATH_KEY, storage_file_path)

            ensure_folder_exists(CONFIG_FOLDER_PATH)
            save_json({STORAGE_FILE_PATH_KEY: storage_file_path}, os.path.join(CONFIG_FOLDER_PATH, CONFIG_NAME))
        except Exception as e:
            logger.error(f"Error during setup of storage file: {e}")

    def _load_storage_file(self) -> bool:
        try:
            config = load_json(os.path.join(CONFIG_FOLDER_PATH, CONFIG_NAME))
            if not config:
                return False
            storage_file_path = config[STORAGE_FILE_PATH_KEY]
            self._storage = KeyValueStorage(storage_file_path)

            storage_file_path2 = self._storage.get(STORAGE_FILE_PATH_KEY)
            if storage_file_path == storage_file_path2:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error during load of storage file: {e}")
            return False

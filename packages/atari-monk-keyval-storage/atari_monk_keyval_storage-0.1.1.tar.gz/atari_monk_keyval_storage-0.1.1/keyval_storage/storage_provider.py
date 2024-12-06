import os
from dataclasses import dataclass
from cli_logger.logger import setup_logger
from pytoolbox.folder import ensure_folder_exists
from keyval_storage.constants import APP_DATA_FOLDER_KEY, KEY_VALUE_STORAGE_PATH_KEY
from keyval_storage.key_value_storage import KeyValueStorage
from keyval_storage.config import logger_config

logger = setup_logger(__name__, logger_config)

@dataclass
class StorageConfig:
    storage_file_name: str

class StorageProvider:
    def __init__(self, config: StorageConfig):
        self._config = config
        self._storage_file_name = config.storage_file_name

    def load_storage(self, storage_path: str) -> KeyValueStorage | None:
        try:
            storage = KeyValueStorage(storage_path)

            storage_path_from_storage = storage.get(KEY_VALUE_STORAGE_PATH_KEY)
            
            if storage_path == storage_path_from_storage:
                return storage
            else:
                logger.error(f"Error when loading storage file - {storage_path}: Storage failed data check.")
                return None   
        except Exception as e:
            logger.exception(f"Error when loading storage file - {storage_path}: {e}")
            return None

    def save_storage(self) -> tuple[KeyValueStorage, str]:
        try:
            data_folder_path = input("Provide PATH for cli_tool DATA FOLDER:> ").strip()
            ensure_folder_exists(data_folder_path)

            storage_file_path = os.path.join(data_folder_path, self._storage_file_name)

            storage = KeyValueStorage(storage_file_path)
            
            storage.set(APP_DATA_FOLDER_KEY, data_folder_path)
            storage.set(KEY_VALUE_STORAGE_PATH_KEY, storage_file_path)

            return storage, storage_file_path
        except Exception as e:
            logger.exception(f"Error when saving storage file: {e}")

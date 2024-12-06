from dataclasses import dataclass
import os
from cli_logger.logger import setup_logger
from pytoolbox.folder import ensure_folder_exists
from pytoolbox.json import save_json, load_json
from keyval_storage.config import logger_config

logger = setup_logger(__name__, logger_config)

@dataclass
class PathData:
    config_folder_path: str
    config_file_name: str

class ConfigProvider:
    def __init__(self, path_data: PathData):
        self._folder_path = path_data.config_folder_path
        self._full_path = os.path.join(self._folder_path, path_data.config_file_name)

    def load_file(self) -> dict | None:
        try:
            config_data = load_json(self._full_path)
        except Exception as e:
            logger.exception(f"Error when loading config file - {self._full_path}: {e}")
        return config_data

    def save_file(self, data: dict):
        try:
            ensure_folder_exists(self._folder_path)

            save_json(data, self._full_path)

        except Exception as e:
            logger.exception(f"Error when saving config file - {self._full_path}: {e}")

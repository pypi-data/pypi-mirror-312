import json
import os
from threading import Lock

class KeyValueStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock = Lock()
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def _read_data(self):
        with self.lock:
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                raise ValueError("Corrupted JSON file")

    def _write_data(self, data):
        with self.lock:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)

    def get(self, key: str):
        data = self._read_data()
        return data.get(key, None)

    def set(self, key: str, value):
        data = self._read_data()
        data[key] = value
        self._write_data(data)

    def delete(self, key: str):
        data = self._read_data()
        if key in data:
            del data[key]
            self._write_data(data)

    def list_keys(self):
        data = self._read_data()
        return list(data.keys())
    
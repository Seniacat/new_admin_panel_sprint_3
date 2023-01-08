import json
from typing import Any, Optional


class JsonFileStorage:
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as outfile:
            json.dump(state, outfile)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path) as file:
                data = json.load(file)
        except FileNotFoundError:
            data = dict()
        return data


class State:
    def __init__(self, storage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        data = self.storage.retrieve_state()
        data[key] = value
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        data = self.storage.retrieve_state()
        return data.get(key)

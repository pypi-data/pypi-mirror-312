import os
import pytest
from keyval_storage.key_value_storage import KeyValueStorage

@pytest.fixture
def temp_file(tmpdir):
    return os.path.join(tmpdir, "test.json")

def test_set_and_get(temp_file):
    storage = KeyValueStorage(temp_file)
    storage.set("key1", "value1")
    assert storage.get("key1") == "value1"

def test_delete(temp_file):
    storage = KeyValueStorage(temp_file)
    storage.set("key1", "value1")
    storage.delete("key1")
    assert storage.get("key1") is None

def test_list_keys(temp_file):
    storage = KeyValueStorage(temp_file)
    storage.set("key1", "value1")
    storage.set("key2", "value2")
    assert set(storage.list_keys()) == {"key1", "key2"}

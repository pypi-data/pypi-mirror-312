import json
import os
import pytest
from pytoolbox.json import load_json, save_json

@pytest.fixture
def temp_file():
    temp_file_path = 'test.json'
    yield temp_file_path
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

def test_save_json(temp_file):
    data = {"name": "Alice", "age": 25}
    save_json(data, temp_file)
    
    assert os.path.exists(temp_file)
    
    with open(temp_file, 'r') as f:
        loaded_data = json.load(f)
    
    assert loaded_data == data

def test_load_json(temp_file):
    data = {"name": "Bob", "age": 30}
    save_json(data, temp_file)
    
    loaded_data = load_json(temp_file)
    
    assert loaded_data == data

def test_load_json_non_existing_file():
    assert load_json('non_existing_file.json') is None

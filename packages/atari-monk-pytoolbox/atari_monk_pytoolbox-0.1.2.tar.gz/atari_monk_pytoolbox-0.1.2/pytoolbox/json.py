import json

def save_json(data: dict, file_path: str) -> None:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2, separators=(',', ': '), ensure_ascii=False)

def load_json(file_path: str) -> dict | None:
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except Exception:
        return None

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[2]
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

def db_path(filename: str) -> Path:
    return DB_DIR / filename

def read_json(filename: str, default: Any):
    path = db_path(filename)
    if not path.exists():
        write_json(filename, default)
        return default
    with open(path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return default

def write_json(filename: str, data: Any):
    path = db_path(filename)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

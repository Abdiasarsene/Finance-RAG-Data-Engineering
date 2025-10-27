# json_validator/schema_loader.py
import json
from pathlib import Path

SCHEMA_PATH = Path("./configs/schema_json.json")

def load_base_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
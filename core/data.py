import json
from core.s3sync import sync_down, sync_up

JSON_PATH = "json/x.json"

def load_data():
    sync_down(JSON_PATH)
    with open(JSON_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)
    sync_up(JSON_PATH)

import json

JSON_PATH = "json/x.json"

def load_data():
    with open(JSON_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)

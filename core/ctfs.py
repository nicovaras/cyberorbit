import os
import json

CTF_PATH = "json/ctfs.json"

def load_ctfs():
    if not os.path.exists(CTF_PATH):
        return []
    with open(CTF_PATH, "r") as f:
        return json.load(f)

def save_ctfs(ctfs):
    with open(CTF_PATH, "w") as f:
        json.dump(ctfs, f, indent=2)

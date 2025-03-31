import os
import json
from core.s3sync import sync_down, sync_up

CTF_PATH = "json/ctfs.json"

def load_ctfs():
    sync_down(CTF_PATH)
    if not os.path.exists(CTF_PATH):
        return []
    with open(CTF_PATH, "r") as f:
        return json.load(f)

def save_ctfs(ctfs):
    with open(CTF_PATH, "w") as f:
        json.dump(ctfs, f, indent=2)
    sync_up(CTF_PATH)
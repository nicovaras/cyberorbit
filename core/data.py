# cyberorbit/core/data.py
import json
import os # <<< Added import
from core.s3sync import sync_down, sync_up

JSON_DIR = "json" # Define base directory

# Ensure the directory exists
os.makedirs(JSON_DIR, exist_ok=True)

# <<< Modified function >>>
def load_data(filename="x.json"):
    """Loads node data from the specified JSON file."""
    # Basic validation to prevent loading unintended files
    if filename not in ["x.json", "y.json"]: # Only allow known files
        filename = "x.json" # Default to x.json if invalid

    file_path = os.path.join(JSON_DIR, filename)
    sync_down(file_path) # Sync down the specific file
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Data file '{file_path}' not found. Returning empty list.")
        # Return a default structure or raise an error if preferred
        return []
    except json.JSONDecodeError:
        print(f"Warning: Error decoding JSON from '{file_path}'. Returning empty list.")
        return []


# <<< Modified function >>>
def save_data(data, filename="x.json"):
    """Saves node data to the specified JSON file."""
     # Basic validation
    if filename not in ["x.json", "y.json"]:
        filename = "x.json"

    file_path = os.path.join(JSON_DIR, filename)
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        sync_up(file_path) # Sync up the specific file
    except IOError as e:
        print(f"Error saving data to '{file_path}': {e}")
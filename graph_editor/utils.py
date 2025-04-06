# yourapp/editor/utils.py
import uuid

def generate_unique_id():
  """Generates a unique string ID."""
  # Using hex representation of UUID4 for a shorter string ID
  return uuid.uuid4().hex
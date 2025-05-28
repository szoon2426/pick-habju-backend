import json
from pathlib import Path

ROOMS_FILE = Path(__file__).resolve().parent.parent / "data" / "rooms.json"

def load_rooms():
    with open(ROOMS_FILE, encoding="utf-8") as f:
        return json.load(f)

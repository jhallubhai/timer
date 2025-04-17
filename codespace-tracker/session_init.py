import os
import json
from datetime import datetime

TRACKER_DIR = os.path.join(os.getcwd(), ".codespace-tracker")
FIRST_START_FILE = os.path.join(TRACKER_DIR, "first_start.json")
CURRENT_SESSION_FILE = os.path.join(TRACKER_DIR, "current_session.json")

def get_now():
    return datetime.utcnow().isoformat()

def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path) as f:
            return json.load(f)
    return {}

def ensure_tracker_dir():
    if not os.path.exists(TRACKER_DIR):
        os.makedirs(TRACKER_DIR)

def main():
    ensure_tracker_dir()
    now = get_now()

    # 1️⃣ First start: only if file doesn't exist
    if not os.path.exists(FIRST_START_FILE):
        print("📌 Creating first_start.json for the very first time...")
        write_json(FIRST_START_FILE, {"first_start": now})
    else:
        print("🕰️ first_start.json already exists. Skipping creation.")

    # 2️⃣ Create/update current_session.json
    print("🔁 Initializing current_session.json...")
    session_data = {
        "date": now.split("T")[0],
        "start_time": now,
        "minutes": 0  # Will be updated every minute by update_minute.py
    }
    write_json(CURRENT_SESSION_FILE, session_data)
    print("✅ current_session.json initialized.")

if __name__ == "__main__":
    main()

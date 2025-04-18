import os
from datetime import datetime
from utils import read_json, write_json, ensure_tracker_dir, append_log

# Constants
TRACKER_DIR = os.path.join(os.getcwd(), ".codespace-tracker")
FIRST_START_FILE = os.path.join(TRACKER_DIR, "first_start.json")
CURRENT_SESSION_FILE = os.path.join(TRACKER_DIR, "current_session.json")

# Ensure directory exists
ensure_tracker_dir()

now = datetime.now().isoformat()

# --- Handle first_start.json ---
first_start_data = read_json(FIRST_START_FILE)

if not first_start_data or "start_time" not in first_start_data:
    print("🌟 Creating first_start.json for the first time...")
    first_start_data = {"start_time": now}
    write_json(FIRST_START_FILE, first_start_data)
    append_log("✅ first_start.json created.")
else:
    print("🕰️ first_start.json already exists with data.")

# --- Handle current_session.json ---
print("🔁 Initializing current_session.json...")
session_data = {
    "start_time": now,
    "last_updated": now,
    "minutes": 0
}
write_json(CURRENT_SESSION_FILE, session_data)
append_log("✅ current_session.json initialized.")

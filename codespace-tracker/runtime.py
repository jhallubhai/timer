import os
import json
from datetime import datetime

TRACKER_DIR = os.path.join(os.getcwd(), ".codespace-tracker")
CURRENT_SESSION_FILE = os.path.join(TRACKER_DIR, "current_session.json")
MINUTE_RUNTIME_FILE = os.path.join(TRACKER_DIR, "minute_runtime.json")
SESSION_LOGS_FILE = os.path.join(TRACKER_DIR, "session_logs.json")

def read_json(path):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error reading {path}: {e}")
    return {}

def write_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"❌ Error writing to {path}: {e}")

def get_now():
    return datetime.utcnow().isoformat()

def update_session_logs():
    current_session = read_json(CURRENT_SESSION_FILE)
    minute_runtime = read_json(MINUTE_RUNTIME_FILE)
    logs = read_json(SESSION_LOGS_FILE)

    # Validate session + runtime data
    if "start_time" not in current_session or "minutes" not in minute_runtime:
        print("❌ Required data missing. Skipping session log update.")
        return

    # Ensure logs is a list
    if not isinstance(logs, list):
        logs = []

    # Prepare log entry
    start_time = current_session["start_time"]
    end_time = get_now()
    minutes = minute_runtime["minutes"]

    log_entry = {
        "start_time": start_time,
        "end_time": end_time,
        "duration_minutes": minutes
    }

    logs.append(log_entry)
    write_json(SESSION_LOGS_FILE, logs)
    print(f"📦 Session logged: {minutes} minutes from {start_time} to {end_time}")

def main():
    update_session_logs()

if __name__ == "__main__":
    main()

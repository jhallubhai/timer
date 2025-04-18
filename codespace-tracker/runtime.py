import os
import json
from datetime import datetime
from dateutil import parser

TRACKER_DIR = os.path.join(os.getcwd(), ".codespace-tracker")
CURRENT_SESSION_FILE = os.path.join(TRACKER_DIR, "current_session.json")
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

def calculate_duration_minutes(start, end):
    start_dt = parser.isoparse(start)
    end_dt = parser.isoparse(end)
    return int((end_dt - start_dt).total_seconds() // 60)

def update_session_logs():
    current_session = read_json(CURRENT_SESSION_FILE)
    logs = read_json(SESSION_LOGS_FILE)

    # Validation
    if "start_time" not in current_session:
        print("❌ start_time missing in current_session.json")
        return

    session_id = current_session.get("session_id", "unknown")
    start_time = current_session["start_time"]
    end_time = datetime.utcnow().isoformat()
    duration_minutes = calculate_duration_minutes(start_time, end_time)

    if not isinstance(logs, list):
        logs = []

    log_entry = {
        "session_id": session_id,
        "start_time": start_time,
        "end_time": end_time,
        "duration_minutes": duration_minutes,
        "recovered": False,
        "date": datetime.utcnow().date().isoformat()
    }

    logs.append(log_entry)
    write_json(SESSION_LOGS_FILE, logs)

    print(f"📦 Session logged: {duration_minutes} mins | ID: {session_id} | From {start_time} to {end_time}")

def main():
    update_session_logs()

if __name__ == "__main__":
    main()

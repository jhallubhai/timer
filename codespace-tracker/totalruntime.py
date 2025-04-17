import os
import json
from datetime import datetime

TRACKER_DIR = os.path.join(os.getcwd(), ".codespace-tracker")
SESSION_LOGS_FILE = os.path.join(TRACKER_DIR, "session_logs.json")
TOTAL_RUNTIME_FILE = os.path.join(TRACKER_DIR, "total_runtime.json")

def read_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def get_now():
    return datetime.utcnow().isoformat()

def calculate_total_runtime():
    logs = read_json(SESSION_LOGS_FILE)

    total_minutes = sum(session.get("duration_minutes", 0) for session in logs)
    total_hours = round(total_minutes / 60, 2)

    stats = {
        "total_minutes": total_minutes,
        "total_hours": total_hours,
        "last_updated": get_now()
    }

    write_json(TOTAL_RUNTIME_FILE, stats)
    print(f"🔄 Total runtime updated: {total_minutes} minutes ({total_hours} hours)")

def main():
    calculate_total_runtime()

if __name__ == "__main__":
    main()

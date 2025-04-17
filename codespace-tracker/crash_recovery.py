import os
import json
from datetime import datetime, timedelta

TRACKER_DIR = os.path.join(os.getcwd(), ".codespace-tracker")
CURRENT_SESSION_FILE = os.path.join(TRACKER_DIR, "current_session.json")
MINUTE_RUNTIME_FILE = os.path.join(TRACKER_DIR, "minute_runtime.json")
SESSION_LOGS_FILE = os.path.join(TRACKER_DIR, "session_logs.json")
DEBUG_LOG = os.path.join(TRACKER_DIR, "debug.log")

def read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def append_log(message):
    with open(DEBUG_LOG, "a") as log:
        log.write(f"[{datetime.now().isoformat()}] {message}\n")

def recover_if_crashed():
    session = read_json(CURRENT_SESSION_FILE)
    minute_data = read_json(MINUTE_RUNTIME_FILE)
    logs = read_json(SESSION_LOGS_FILE)

    # Crash recovery logic
    if session and minute_data:
        start_time = session.get("start_time")
        date = session.get("date")
        minutes = minute_data.get("minutes", 0)

        if start_time and minutes > 0:
            recovered_session = {
                "start_time": start_time,
                "end_time": datetime.utcnow().isoformat(),
                "duration_minutes": minutes,
                "recovered": True,
                "date": date
            }
            logs.append(recovered_session)
            write_json(SESSION_LOGS_FILE, logs)

            append_log(f"🛠️ Recovered crashed session of {minutes} minutes starting from {start_time}")
            print("🛠️ Crash recovery successful. Session log updated.")

            # Reset session + minute_runtime
            write_json(CURRENT_SESSION_FILE, {})
            write_json(MINUTE_RUNTIME_FILE, {"minutes": 0})
        else:
            append_log("✅ No recovery needed. All clean.")
    else:
        append_log("✅ No recovery needed. Files empty.")

def main():
    recover_if_crashed()

if __name__ == "__main__":
    main()

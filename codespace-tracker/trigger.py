import os
import time
import json
from datetime import datetime, timedelta

TRACKER_DIR = os.path.join(os.getcwd(), ".codespace-tracker")
MINUTE_RUNTIME_FILE = os.path.join(TRACKER_DIR, "minute_runtime.json")
SESSION_LOGS_FILE = os.path.join(TRACKER_DIR, "session_logs.json")
TOTAL_RUNTIME_FILE = os.path.join(TRACKER_DIR, "total_runtime.json")
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

def monitor_and_trigger():
    while True:
        # Read the necessary files
        minute_data = read_json(MINUTE_RUNTIME_FILE)
        session_logs = read_json(SESSION_LOGS_FILE)
        total_runtime = read_json(TOTAL_RUNTIME_FILE)

        # Monitor the minute_runtime
        minutes = minute_data.get("minutes", 0)
        total_minutes = total_runtime.get("total_minutes", 0)

        # Log status in debug log
        append_log(f"🕒 Monitoring... Current session time: {minutes} minutes, Total runtime: {total_minutes} minutes.")

        # Trigger actions based on conditions
        if minutes >= 25:  # If a season is complete (25 minutes)
            append_log(f"✅ 25 minutes reached. Starting backup or new session...")
            trigger_backup_or_next_season(minutes)

        # Update total runtime every 25 minutes
        if minutes % 25 == 0 and minutes > 0:
            total_runtime["total_minutes"] += minutes
            write_json(TOTAL_RUNTIME_FILE, total_runtime)
            append_log(f"Total runtime updated: {total_runtime['total_minutes']} minutes.")

        # Wait for next minute
        time.sleep(60)

def trigger_backup_or_next_season(minutes):
    # Here you can trigger any backup process or session update
    session_logs = read_json(SESSION_LOGS_FILE)

    # Update the session log
    new_session_log = {
        "start_time": datetime.utcnow().isoformat(),
        "end_time": (datetime.utcnow() + timedelta(minutes=minutes)).isoformat(),
        "duration_minutes": minutes,
        "recovered": False,
        "date": datetime.utcnow().date().isoformat()
    }
    session_logs.append(new_session_log)

    # Save updated session logs
    write_json(SESSION_LOGS_FILE, session_logs)

    # Reset minute_runtime
    write_json(MINUTE_RUNTIME_FILE, {"minutes": 0})

    append_log(f"📝 Session completed and logged. Starting a new session...")

def main():
    monitor_and_trigger()

if __name__ == "__main__":
    main()

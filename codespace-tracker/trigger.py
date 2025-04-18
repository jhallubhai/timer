import os
import time
import json
from datetime import datetime

TRACKER_DIR = os.path.join(os.getcwd(), ".codespace-tracker")
MINUTE_RUNTIME_FILE = os.path.join(TRACKER_DIR, "minute_runtime.json")
TOTAL_RUNTIME_FILE = os.path.join(TRACKER_DIR, "total_runtime.json")
DEBUG_LOG = os.path.join(TRACKER_DIR, "debug.log")

def read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

def append_log(message):
    with open(DEBUG_LOG, "a") as log:
        log.write(f"[{datetime.now().isoformat()}] {message}\n")

def monitor_and_trigger():
    last_triggered_10 = False
    last_triggered_25 = False

    while True:
        minute_data = read_json(MINUTE_RUNTIME_FILE)
        total_runtime = read_json(TOTAL_RUNTIME_FILE)

        minutes = minute_data.get("minutes", 0)
        total_minutes = total_runtime.get("total_minutes", 0)

        print(f"👀 Watching... {minutes} minutes elapsed.")
        append_log(f"🕒 Monitoring... Session time: {minutes}, Total time: {total_minutes}")

        # 10-min condition
        if minutes >= 10 and not last_triggered_10:
            print("🚀 Triggered: 10-minute milestone!")
            append_log("🚀 Trigger hit: 10 minutes mark.")
            # Example: os.system("bash backup.sh")
            last_triggered_10 = True

        # 25-min condition
        if minutes >= 25 and not last_triggered_25:
            print("🎯 Triggered: 25-minute milestone! Time to perform action!")
            append_log("🎯 Trigger hit: 25 minutes mark.")
            # Example: os.system("python runtime.py")
            last_triggered_25 = True

        # Reset flags if session resets
        if minutes == 0:
            last_triggered_10 = False
            last_triggered_25 = False

        time.sleep(60)

def main():
    monitor_and_trigger()

if __name__ == "__main__":
    main()

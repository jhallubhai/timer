#!/bin/bash

echo ""
echo "🔧 Starting Codespace Tracker Setup..."

# 1. Create tracker directory if not exists
TRACKER_DIR=".codespace-tracker"

if [ ! -d "$TRACKER_DIR" ]; then
    echo "📁 Creating tracker directory: $TRACKER_DIR"
    mkdir -p "$TRACKER_DIR"
else
    echo "📁 Tracker directory already exists."
fi

# 2. Create JSON files if not exists
declare -a files=("first_start.json" "current_session.json" "minute_runtime.json" "session_logs.json" "total_runtime.json" "debug.log")

for file in "${files[@]}"
do
    path="$TRACKER_DIR/$file"
    if [ ! -f "$path" ]; then
        echo "📄 Creating $file"
        if [[ $file == *.json ]]; then
            echo "{}" > "$path"
        else
            touch "$path"
        fi
    else
        echo "✅ $file already exists."
    fi
done

# 3. Install dependencies (optional if using Codespaces with Python pre-installed)
echo "📦 Checking Python and pip..."
python3 --version >/dev/null 2>&1 || { echo "❌ Python3 not found!"; exit 1; }
pip3 --version >/dev/null 2>&1 || { echo "❌ pip3 not found!"; exit 1; }

# 4. Call start_all.sh to launch background scripts
if [ -f "start_all.sh" ]; then
    echo "🚀 Starting all background trackers via start_all.sh..."
    bash start_all.sh
else
    echo "❌ start_all.sh not found!"
    exit 1
fi

echo ""
echo "✅ Codespace Tracker setup complete!"

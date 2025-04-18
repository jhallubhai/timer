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

# 2. Create JSON/log files (first_start.json will be handled by session_init.py)
declare -a files=("current_session.json" "minute_runtime.json" "session_logs.json" "total_runtime.json" "debug.log")

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

# Check for Python 3
python3 --version >/dev/null 2>&1 || { echo "❌ Python3 not found!"; exit 1; }

# Check for pip3
if ! command -v pip3 >/dev/null 2>&1; then
    echo "⚠️ pip3 not found. Attempting to install..."
    
    # Update package list
    sudo apt update

    # Install pip3 (Debian/Ubuntu)
    sudo apt install -y python3-pip || { echo "❌ Failed to install pip3!"; exit 1; }

    echo "✅ pip3 installed successfully."
else
    echo "✅ pip3 is already installed."
fi

# Install or upgrade dependencies
echo "📦 Installing/upgrading dependencies from requirements.txt..."
pip3 install --upgrade -r requirements.txt


# 4. Initialize first_start.json and current_session.json via session_init.py
echo "⚙️ Initializing session with session_init.py..."
python3 session_init.py

# 5. Create runtime loop scripts if not exist

chmod +x runtime_loop.sh totalruntime_loop.sh

# 6. Launch background trackers
echo "🚀 Starting all background trackers via start_all.sh..."
bash start_all.sh

echo ""
echo "✅ Codespace Tracker setup complete!"

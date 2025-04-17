#!/bin/bash

echo ""
echo "🚀 Codespace Session Start Triggered..."

# Define paths
SESSION_INIT="$(pwd)/session_init.py"
CRASH_RECOVERY="$(pwd)/crash_recovery.py"

# Check and run crash recovery first
if [ -f "$CRASH_RECOVERY" ]; then
    echo "💣 Running crash recovery..."
    python3 "$CRASH_RECOVERY"
else
    echo "⚠️ crash_recovery.py not found at $CRASH_RECOVERY"
fi

# Then run session initializer
if [ -f "$SESSION_INIT" ]; then
    echo "📌 Initializing new session..."
    python3 "$SESSION_INIT"
else
    echo "❌ session_init.py not found at $SESSION_INIT"
    exit 1
fi

echo "✅ Session initialized successfully!"

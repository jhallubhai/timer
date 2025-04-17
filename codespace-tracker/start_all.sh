#!/bin/bash

echo ""
echo "🚀 Starting all services for Codespace Tracker..."

# Start ghadi.sh
echo "⏰ Starting clock (ghadi.sh)..."
nohup ./ghadi.sh > ghadi.log 2>&1 &

# Start runtime.py (20 min interval)
echo "⏳ Starting runtime.py (updates every 20 minutes)..."
nohup python3 "$(pwd)/runtime.py" > runtime.log 2>&1 &

# Start totalruntime.py (25 min interval)
echo "📊 Starting totalruntime.py (updates every 25 minutes)..."
nohup python3 "$(pwd)/totalruntime.py" > totalruntime.log 2>&1 &

# Start trigger.py (always watching)
echo "🔁 Starting trigger.py (always running in background)..."
nohup python3 "$(pwd)/trigger.py" > trigger.log 2>&1 &

echo "✅ All services are now running! Codespace tracker is active."

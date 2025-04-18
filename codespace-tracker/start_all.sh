#!/bin/bash

echo ""
echo "🚀 Starting all services for Codespace Tracker..."

# Start ghadi.sh
echo "⏰ Starting clock (ghadi.sh)..."
nohup ./ghadi.sh > ghadi.log 2>&1 &

# Start runtime_loop.sh (every 20 mins)
echo "⏳ Starting runtime_loop.sh (every 20 minutes)..."
nohup bash "$(pwd)/runtime_loop.sh" > runtime_loop.log 2>&1 &

# Start totalruntime_loop.sh (every 25 mins)
echo "📊 Starting totalruntime_loop.sh (every 25 minutes)..."
nohup bash "$(pwd)/totalruntime_loop.sh" > totalruntime_loop.log 2>&1 &

# Start trigger.py (always watching)
echo "🔁 Starting trigger.py (always running in background)..."
nohup python3 "$(pwd)/trigger.py" > trigger.log 2>&1 &

echo "✅ All services are now running! Codespace tracker is active."

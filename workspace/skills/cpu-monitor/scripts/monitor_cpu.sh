#!/bin/bash

# Configuration
CPU_THRESHOLD=30 # Alert if CPU usage goes above this percentage

# Get current CPU usage (active percentage)
# This command extracts the idle percentage from 'top' and subtracts it from 100
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

# Check if CPU_USAGE is a number
if ! [[ "$CPU_USAGE" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    MESSAGE="[CPU Monitor] Error: Could not get CPU usage. Output: $CPU_USAGE"
    openclaw sessions send --message "$MESSAGE" --session-key "telegram:6202550149"
    exit 1
fi

# Compare with threshold
if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
    MESSAGE="[CPU Alert] 📈 High CPU usage: ${CPU_USAGE}%! (Threshold: ${CPU_THRESHOLD}%)"
    # Send message to the current OpenClaw session
    openclaw sessions send --message "$MESSAGE" --session-key "telegram:6202550149"
fi

# Always print current CPU usage
echo "Current CPU usage: ${CPU_USAGE}%"

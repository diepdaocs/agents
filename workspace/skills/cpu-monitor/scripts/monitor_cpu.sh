#!/bin/bash

# Configuration
CPU_THRESHOLD=30 # Alert if CPU usage goes above this percentage

# Get current CPU usage (active percentage)
# This command extracts the idle percentage from 'top' and subtracts it from 100
CPU_USAGE=$(/usr/bin/top -bn1 | /usr/bin/grep "Cpu(s)" | /usr/bin/sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | /usr/bin/awk '{print 100 - $1}')

# Check if CPU_USAGE is a number
if ! [[ "$CPU_USAGE" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    MESSAGE="[CPU Monitor] Error: Could not get CPU usage. Output: $CPU_USAGE"
    openclaw sessions send --message "$MESSAGE" --agent-id "main"
    exit 1
fi

# Compare with threshold
if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
    MESSAGE="[CPU Alert] 📈 High CPU usage: ${CPU_USAGE}%! (Threshold: ${CPU_THRESHOLD}%)"
    # Send message to the current OpenClaw session
    openclaw sessions send --message "$MESSAGE" --agent-id "main"
fi

# Always print current CPU usage
echo "Current CPU usage: ${CPU_USAGE}%"

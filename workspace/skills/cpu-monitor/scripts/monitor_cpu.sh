#!/bin/bash

# Configuration
CPU_THRESHOLD=70 # Alert if CPU usage goes above this percentage

# Get current CPU usage using /proc/stat (two samples 1 second apart for accuracy)
read_cpu() {
    awk '/^cpu / {print $2+$3+$4+$5+$6+$7+$8, $5}' /proc/stat
}
SAMPLE1=$(read_cpu); sleep 1; SAMPLE2=$(read_cpu)
TOTAL1=$(echo $SAMPLE1 | awk '{print $1}'); IDLE1=$(echo $SAMPLE1 | awk '{print $2}')
TOTAL2=$(echo $SAMPLE2 | awk '{print $1}'); IDLE2=$(echo $SAMPLE2 | awk '{print $2}')
CPU_USAGE=$(awk "BEGIN {dt=$TOTAL2-$TOTAL1; di=$IDLE2-$IDLE1; printf \"%.1f\", (dt-di)/dt*100}")

# Check if CPU_USAGE is a number
if ! [[ "$CPU_USAGE" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    MESSAGE="[CPU Monitor] Error: Could not get CPU usage. Output: $CPU_USAGE"
    openclaw message send --target "telegram:6202550149" --message "$MESSAGE"
    exit 1
fi

# Compare with threshold
if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
    # Get top 5 processes by CPU usage
    TOP_PROCESSES=$(ps aux --sort=-%cpu | head -n 6)
    MESSAGE="[CPU Alert] 📈 High CPU usage: ${CPU_USAGE}%! (Threshold: ${CPU_THRESHOLD}%)\n\nTop 5 processes by CPU usage:\n\`\`\`\n$TOP_PROCESSES\n\`\`\`"
    # Send message to Telegram
    openclaw message send --target "telegram:6202550149" --message "$MESSAGE"
fi

# Always print current CPU usage
echo "Current CPU usage: ${CPU_USAGE}%"

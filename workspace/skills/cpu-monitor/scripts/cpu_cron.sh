#!/bin/bash

# CPU Monitor - Direct execution version for cron
# This script runs the CPU check and sends alerts if needed

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/monitor_cpu.sh"

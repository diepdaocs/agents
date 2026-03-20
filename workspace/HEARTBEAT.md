# Heartbeat

Tasks to run on each heartbeat. Keep this empty (or comments only) to skip heartbeat API calls.

<!-- Example tasks:
- Check if any background coding jobs have finished and summarize results
- Review memory/today.md and flag anything that needs follow-up
- Check git status on active projects and note any uncommitted changes
-->

## CPU Monitor
- On system event "run_cpu_check": execute `~/code/agents/workspace/skills/cpu-monitor/scripts/monitor_cpu.sh`
- Script alerts via Telegram if CPU > 50% threshold
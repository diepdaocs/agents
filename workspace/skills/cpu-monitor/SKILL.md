---
name: cpu-monitor
description: Monitor PC CPU usage and alert if it exceeds a specified threshold. Use when: (1) You need to regularly check CPU load, (2) Receive alerts for high CPU usage (e.g., >95%), (3) Set up periodic performance checks.
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["bash", "grep", "sed", "awk"] },
      },
  }
---

# CPU Monitor Skill

This skill provides a script and instructions to monitor your PC's CPU usage and send an alert if it goes above a predefined threshold.

## How to Use

1.  **CPU Monitoring Script**:
    The `monitor_cpu.sh` script (located in `scripts/`) will check the current CPU usage.

2.  **Configuration**:
    You can adjust the `CPU_THRESHOLD` within the `monitor_cpu.sh` script. The default is 95%.

3.  **Set up a Cron Job**:
    To run the monitor every 5 minutes and receive alerts, set up a cron job.
    First, ensure the script is executable:
    ```bash
    chmod +x ~/code/agents/workspace/skills/cpu-monitor/scripts/monitor_cpu.sh
    ```
    Then, add the following line to your crontab (run `crontab -e`):
    ```cron
    */5 * * * * /home/noname/code/agents/workspace/skills/cpu-monitor/scripts/monitor_cpu.sh
    ```
    This will execute the script every 5 minutes. If the CPU usage is above the threshold, an alert will be sent to the current session.

## `monitor_cpu.sh` Script Details

The script uses `top`, `grep`, `sed`, and `awk` to get the idle CPU percentage and then calculates the active CPU percentage. If it's above the `CPU_THRESHOLD`, it sends a message to the OpenClaw session.

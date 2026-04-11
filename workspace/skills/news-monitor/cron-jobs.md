# News Monitor Cron Jobs

## Scheduled Delivery Times
- 7:00 AM SGT: Morning brief
- 7:00 PM SGT: Evening brief

## Cron Schedule
```
# 7:00 AM SGT
0 7 * * * python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py morning

# 7:00 PM SGT
0 19 * * * python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py evening
```

## Installation
1. Copy cron lines to crontab: `crontab -e`
2. Ensure scripts have execute permissions: `chmod +x *.sh`
3. Configure Telegram bot token and chat ID in send-telegram.sh

## Monitoring
Check logs in /var/log/news-monitor.log for delivery status.
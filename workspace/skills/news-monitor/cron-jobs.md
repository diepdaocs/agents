# News Monitor Cron Jobs

## Scheduled Delivery Times
- 7:30 AM SGT: Morning brief
- 1:00 PM SGT: Midday update  
- 7:00 PM SGT: Evening brief
- 10:00 PM SGT: Night brief

## Cron Schedule
```
# 7:30 AM SGT (23:30 UTC previous day)
30 23 * * * /home/noname/code/agents/workspace/skills/news-monitor/scripts/fetch-and-send.sh morning

# 1:00 PM SGT (05:00 UTC)
0 5 * * * /home/noname/code/agents/workspace/skills/news-monitor/scripts/fetch-and-send.sh midday

# 7:00 PM SGT (11:00 UTC)
0 11 * * * /home/noname/code/agents/workspace/skills/news-monitor/scripts/fetch-and-send.sh evening

# 10:00 PM SGT (14:00 UTC)
0 14 * * * /home/noname/code/agents/workspace/skills/news-monitor/scripts/fetch-and-send.sh night
```

## Installation
1. Copy cron lines to crontab: `crontab -e`
2. Ensure scripts have execute permissions: `chmod +x *.sh`
3. Configure Telegram bot token and chat ID in send-telegram.sh

## Monitoring
Check logs in /var/log/news-monitor.log for delivery status.
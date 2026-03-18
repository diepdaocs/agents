---
name: news-monitor
description: "Deliver curated news briefing for 9 topics: HackerNews top stories, engineering blogs (Google/Meta/Microsoft/OpenAI/Anthropic), tech, AI, finance, coffee/robusta futures, blockchain, tennis (Alcaraz), soccer (Barcelona). Sends to Telegram at 7:30 AM, 1 PM, 7 PM, 10 PM SGT. Use when asked to send news briefing, morning/afternoon/evening/night news update, or run news monitor."
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires": { "bins": ["python3"] },
      },
  }
---

# News Monitor

Fetches news from official RSS feeds and APIs only — no junk or fake news. Delivers to Telegram via three messages grouped by theme.

## Topics & Sources

| Topic | Sources |
|-------|---------|
| Tech | TechCrunch, The Verge, Ars Technica, Wired |
| AI | VentureBeat, The Verge AI, MIT Tech Review, Ars Technica |
| HackerNews | HN Algolia API (front_page top stories, scores + comment counts) |
| Engineering Blogs | Google AI Blog, Google Developers, Meta Engineering, Microsoft Dev Blog, OpenAI Blog, Anthropic Blog |
| Finance | The Economist, Bloomberg, Barron's |
| Coffee & Robusta Futures | Reuters Commodities, Reuters Business, Investing.com, VnExpress |
| Blockchain | CoinDesk, CoinTelegraph, Decrypt, TheBlock |
| Tennis (Alcaraz) | ESPN Tennis, BBC Sport Tennis |
| Soccer (Barcelona) | Goal.com, FC Barcelona Official |

**Credibility:** ✅ = Tier-1 (Reuters, BBC, ESPN, CNBC, AP) | ✓ = Tier-2 (TechCrunch, CoinDesk, HN, etc.)

## Message Groups

| Message | Topics |
|---------|--------|
| Part 1 | HackerNews · Engineering Blogs |
| Part 2 | Tech · AI |
| Part 3 | Finance · Coffee & Robusta Futures · Blockchain |
| Part 4 | Tennis · Soccer |

## Execution

Map the user's request to a session:

| Request | Session |
|---------|---------|
| morning briefing / 7:30 AM | `morning` |
| afternoon / midday / 1 PM | `afternoon` |
| evening / 7 PM | `evening` |
| night / 10 PM | `night` |

Run the news monitor:
```bash
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py [session]
```

Examples:
```bash
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py morning
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py afternoon
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py evening
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py night
```

Dry-run (no Telegram send, just print):
```bash
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py morning --test
```

## Delivery Schedule (SGT = UTC+8)

| Time SGT | Session | Cron (UTC) |
|----------|---------|------------|
| 7:30 AM  | morning   | `30 23 * * *` |
| 1:00 PM  | afternoon | `0 5 * * *`   |
| 7:00 PM  | evening   | `0 11 * * *`  |
| 10:00 PM | night     | `0 14 * * *`  |

## Cron Names

- `news-morning`
- `news-afternoon`
- `news-evening`
- `news-night`

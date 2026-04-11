---
name: news-monitor
description: "Deliver a curated Telegram news briefing for 9 topics: HackerNews, engineering blogs, tech, AI, finance, coffee/robusta futures, blockchain, tennis (Alcaraz), and soccer (Barcelona). Fetch the article URLs, summarize the top link per topic, explain why it matters, and send twice daily at 7 AM and 7 PM SGT. Use when asked to send or refactor the news briefing."
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

Fetches news from official RSS feeds first, uses Google News search feeds as fallback discovery when direct feeds are thin, opens the shortlisted article URLs, then sends a concise summary for each topic followed by that topic's top links.

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
| Part 1 | HackerNews · Engineering Blogs · Tech · AI |
| Part 2 | Finance · Coffee & Robusta Futures · Blockchain · Tennis · Soccer |

Each topic should include:
- 1 short topic-level summary synthesized from the top items
- 1 short why-it-matters line for the topic
- top links listed underneath the summary

Source ladder:
1. direct topic feeds / official blogs / direct RSS
2. Google News search RSS for gap-filling and thin topics
3. if filtering is too strict, fall back to the best source-ranked item instead of returning nothing
4. when all top candidates were seen recently, still show the best current item for that topic instead of leaving the section empty

## Execution

Map the user's request to a session:

| Request | Session |
|---------|---------|
| morning briefing / 7 AM | `morning` |
| evening briefing / 7 PM | `evening` |
| daily news briefing | `morning` or `evening` depending on context |

Run the news monitor:
```bash
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py [session]
```

Examples:
```bash
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py morning
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py evening
```

Dry-run (no Telegram send, just print):
```bash
python3 ~/code/agents/workspace/skills/news-monitor/scripts/news_monitor.py morning --test
```

## Delivery Schedule (SGT = UTC+8)

| Time SGT | Session | Cron (SGT local) |
|----------|---------|------------------|
| 7:00 AM  | morning | `0 7 * * *` |
| 7:00 PM  | evening | `0 19 * * *` |

## Cron Names

- `news-morning`
- `news-evening`

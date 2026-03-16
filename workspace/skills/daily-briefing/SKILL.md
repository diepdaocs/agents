---
name: daily-briefing
description: "Morning digest covering weather, pending tasks, recent memory, and any queued cron jobs. Use when: user asks for a daily summary, morning briefing, or 'what's on today'. NOT for: real-time news, stock prices, or calendar data (unless a calendar skill is installed)."
metadata:
  {
    "openclaw":
      {
        "emoji": "🌅",
        "requires": { "bins": ["curl"] },
      },
  }
---

# Daily Briefing Skill

Produce a concise morning digest when the user asks for a briefing, summary, or "what's on today".

## When to Use

✅ **USE this skill when:**

- "Good morning" or "morning briefing"
- "What's on today?" / "What do I have going on?"
- "Give me a daily summary"
- "Catch me up"

## When NOT to Use

❌ **DON'T use this skill when:**

- User wants live news headlines → no reliable source available by default
- User wants calendar events → use a calendar skill if installed
- User wants stock/crypto prices → use a dedicated finance skill

## Briefing Structure

Assemble the briefing in this order, skipping sections with no content:

1. **Weather** — current conditions + today's forecast for the user's location (from USER.md). Use `curl "wttr.in/{city}?format=3"`.
2. **Memory highlights** — scan today's memory file (`memory/YYYY-MM-DD.md`) for anything flagged or unresolved.
3. **Pending tasks** — check HEARTBEAT.md and any task lists mentioned in MEMORY.md.
4. **Scheduled jobs** — run `openclaw cron list` and surface anything due today.

## Format

Keep it scannable. Use short bullets. No prose padding.

```
🌅 Morning Briefing — {Day}, {Date}

☁️ Weather: Hanoi — 28°C, partly cloudy, light breeze

📝 Pending:
• Review PR #42 (noted yesterday)
• Reply to design feedback on landing page

⏰ Scheduled today:
• 09:00 — weekly-report cron
```

## Notes

- If USER.md has no location set, skip weather and note it.
- If memory file doesn't exist yet, skip that section silently.
- Keep the whole briefing under 20 lines.

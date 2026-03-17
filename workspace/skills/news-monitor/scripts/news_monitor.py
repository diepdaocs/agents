#!/usr/bin/env python3
"""
News monitor — fetch curated news and deliver to Telegram.

Usage:
    python3 news_monitor.py [session]  # session: morning|afternoon|evening|night
    python3 news_monitor.py --test     # dry-run: print message, skip Telegram send
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

# Allow importing fetch_news from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_news

# ── Telegram config ──────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = "8625186050:AAGJ-BfSs3v4intvZCg7bH3fGE2SIV-oHcA"
TELEGRAM_CHAT_ID   = "6202550149"
TELEGRAM_API       = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

SGT = timezone(timedelta(hours=8))

SESSION_LABELS = {
    "morning":   "🌅 Morning Briefing",
    "afternoon": "☀️ Afternoon Update",
    "evening":   "🌆 Evening Round-up",
    "night":     "🌙 Night Digest",
}


# ── Telegram delivery ────────────────────────────────────────────────────────

def send_telegram(text):
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }).encode("utf-8")
    req = urllib.request.Request(
        TELEGRAM_API, data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


# ── Message builder ──────────────────────────────────────────────────────────

def build_messages(session="morning"):
    """Build 2 Telegram messages: topics 1-3 and topics 4-6."""
    sgt_now    = datetime.now(SGT)
    time_str   = sgt_now.strftime("%a %b %d %Y · %I:%M %p SGT")
    label      = SESSION_LABELS.get(session, "📰 News Update")

    header = (
        f"📰 <b>NEWS BRIEFING</b> · <b>{label}</b>\n"
        f"<i>{time_str}</i>\n"
    )
    sep = "\n─────────────────────\n"

    print("Fetching news from RSS feeds...", file=sys.stderr)
    results = fetch_news.fetch_all()

    topic_keys = list(fetch_news.TOPICS.keys())  # guaranteed order in 3.7+
    first_half  = topic_keys[:3]   # tech, ai, finance
    second_half = topic_keys[3:]   # blockchain, tennis, soccer

    def build_half(keys, part_label):
        sections = []
        for k in keys:
            items = results.get(k, [])
            sections.append(fetch_news.format_topic_html(k, items))
        body = sep.join(sections)
        msg  = header + f"<b>{part_label}</b>" + sep + body
        foot = f"\n{sep}<i>Official sources only · fact-checked ✅=Tier1 ✓=Tier2</i>"
        return (msg + foot)[:4090]

    msg1 = build_half(first_half,  "Part 1 — Tech · AI · Finance")
    msg2 = build_half(second_half, "Part 2 — Blockchain · Tennis · Soccer")
    return msg1, msg2


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    dry_run = "--test" in sys.argv
    args    = [a for a in sys.argv[1:] if not a.startswith("-")]
    session = args[0] if args else "morning"

    try:
        msg1, msg2 = build_messages(session)
    except Exception as e:
        print(f"❌ Failed to build news message: {e}", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        print("\n" + "=" * 60)
        print("MESSAGE 1:")
        print(msg1)
        print("\n" + "=" * 60)
        print("MESSAGE 2:")
        print(msg2)
        print("=" * 60)
        print("\n[DRY RUN] Telegram send skipped.", file=sys.stderr)
        return

    errors = 0
    for i, msg in enumerate((msg1, msg2), 1):
        try:
            result = send_telegram(msg)
            if result.get("ok"):
                mid = result.get("result", {}).get("message_id", "?")
                print(f"✅ Message {i}/2 sent (message_id={mid})", file=sys.stderr)
            else:
                print(f"❌ Telegram error on msg {i}: {result}", file=sys.stderr)
                errors += 1
        except Exception as e:
            print(f"❌ Send error on msg {i}: {e}", file=sys.stderr)
            errors += 1

    if errors:
        sys.exit(1)
    print("✅ All messages delivered.", file=sys.stderr)


if __name__ == "__main__":
    main()

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

# ── Sent-links dedup cache ────────────────────────────────────────────────────
SENT_CACHE_FILE = os.path.expanduser("~/.openclaw/news_cache/news_sent_links.json")
SENT_CACHE_MAX  = 2000  # keep at most this many links to prevent unbounded growth


def _load_sent_links():
    try:
        with open(SENT_CACHE_FILE) as f:
            data = json.load(f)
        return set(data) if isinstance(data, list) else set()
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def _save_sent_links(links: set):
    os.makedirs(os.path.dirname(SENT_CACHE_FILE), exist_ok=True)
    # Trim to most-recent SENT_CACHE_MAX by keeping a list in insertion order.
    # Since we can't preserve order from a set, just truncate if oversized.
    lst = list(links)
    if len(lst) > SENT_CACHE_MAX:
        lst = lst[-SENT_CACHE_MAX:]
    with open(SENT_CACHE_FILE, "w") as f:
        json.dump(lst, f)


def _filter_new(items, sent_links):
    """Return only items whose link has not been sent before."""
    return [i for i in items if i.get("link") and i["link"] not in sent_links]

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
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read())


# ── Message builder ──────────────────────────────────────────────────────────

GROUPS = [
    (["hackernews", "engblogs"],          "Part 1 — HackerNews · Eng Blogs"),
    (["tech", "ai"],                      "Part 2 — Tech · AI"),
    (["finance", "coffee", "blockchain"], "Part 3 — Finance · Coffee · Blockchain"),
    (["tennis", "soccer"],               "Part 4 — Tennis · Soccer"),
]


def build_messages(session="morning"):
    """Build Telegram messages grouped by theme. Returns (messages, new_links)."""
    sgt_now  = datetime.now(SGT)
    time_str = sgt_now.strftime("%a %b %d %Y · %I:%M %p SGT")
    label    = SESSION_LABELS.get(session, "📰 News Update")

    header = (
        f"📰 <b>NEWS BRIEFING</b> · <b>{label}</b>\n"
        f"<i>{time_str}</i>\n"
    )
    sep = "\n─────────────────────\n"

    print("Fetching news from RSS feeds...", file=sys.stderr)
    results = fetch_news.fetch_all()

    sent_links = _load_sent_links()
    new_links  = set()

    # Filter each topic to only unseen items
    filtered = {}
    for topic_key, items in results.items():
        fresh = _filter_new(items, sent_links)
        filtered[topic_key] = fresh
        for item in fresh:
            if item.get("link"):
                new_links.add(item["link"])

    skipped = sum(len(v) - len(filtered[k]) for k, v in results.items())
    if skipped:
        print(f"[dedup] Skipped {skipped} already-sent item(s).", file=sys.stderr)

    messages = []
    for keys, part_label in GROUPS:
        sections = []
        for k in keys:
            items = filtered.get(k, [])
            sections.append(fetch_news.format_topic_html(k, items))
        body = sep.join(sections)
        msg  = header + f"<b>{part_label}</b>" + sep + body
        foot = f"\n{sep}<i>Official sources only · fact-checked ✅=Tier1 ✓=Tier2</i>"
        messages.append((msg + foot)[:4090])

    return messages, new_links


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    dry_run = "--test" in sys.argv
    args    = [a for a in sys.argv[1:] if not a.startswith("-")]
    session = args[0] if args else "morning"

    try:
        messages, new_links = build_messages(session)
    except Exception as e:
        print(f"❌ Failed to build news message: {e}", file=sys.stderr)
        sys.exit(1)

    total = len(messages)

    if dry_run:
        for i, msg in enumerate(messages, 1):
            print("\n" + "=" * 60)
            print(f"MESSAGE {i}/{total}:")
            print(msg)
        print("=" * 60)
        print("\n[DRY RUN] Telegram send skipped.", file=sys.stderr)
        return

    errors = 0
    for i, msg in enumerate(messages, 1):
        try:
            result = send_telegram(msg)
            if result.get("ok"):
                mid = result.get("result", {}).get("message_id", "?")
                print(f"✅ Message {i}/{total} sent (message_id={mid})", file=sys.stderr)
            else:
                print(f"❌ Telegram error on msg {i}: {result}", file=sys.stderr)
                errors += 1
        except Exception as e:
            print(f"❌ Send error on msg {i}: {e}", file=sys.stderr)
            errors += 1

    if errors:
        sys.exit(1)

    # Persist sent links only after all messages delivered successfully
    sent_links = _load_sent_links()
    sent_links.update(new_links)
    _save_sent_links(sent_links)
    print(f"✅ All messages delivered. Cache updated (+{len(new_links)} links).", file=sys.stderr)


if __name__ == "__main__":
    main()

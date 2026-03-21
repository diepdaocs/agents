#!/usr/bin/env python3
"""Fetch recent crypto news headlines from public RSS feeds. No API key required."""

import json
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# ── Sent-links dedup cache ────────────────────────────────────────────────────
SENT_CACHE_FILE = os.path.expanduser("~/.openclaw/news_cache/crypto_sent_links.json")
SENT_CACHE_MAX  = 1000


def _load_sent_links():
    try:
        with open(SENT_CACHE_FILE) as f:
            data = json.load(f)
        return set(data) if isinstance(data, list) else set()
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def _save_sent_links(links: set):
    os.makedirs(os.path.dirname(SENT_CACHE_FILE), exist_ok=True)
    lst = list(links)
    if len(lst) > SENT_CACHE_MAX:
        lst = lst[-SENT_CACHE_MAX:]
    with open(SENT_CACHE_FILE, "w") as f:
        json.dump(lst, f)

FEEDS = [
    ("CoinDesk",      "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
    ("Decrypt",       "https://decrypt.co/feed"),
    ("TheBlock",      "https://www.theblock.co/rss.xml"),
]

MACRO_KEYWORDS = [
    # Macro / regulation
    "fed ", "federal reserve", "interest rate", "inflation", "cpi", "gdp",
    "recession", "sec ", "etf", "regulation", "ban", "legal", "congress",
    "senate", "treasury", "imf", "world bank", "g20", "g7",
    # Market-moving
    "hack", "exploit", "breach", "liquidat", "crash", "surge", "rally",
    "all-time high", "ath", "dump", "whale", "blackrock", "fidelity",
    "institutional", "bankruptcy", "insolvency", "depegged", "depeg",
    "war", "sanction", "geopolit",
    # Coin-specific macro
    "bitcoin etf", "ethereum etf", "solana etf", "spot etf",
    "halving", "merge", "upgrade", "fork",
]

HEADERS = {"User-Agent": "crypto-monitor-skill/1.0"}
MAX_PER_FEED = 5


def fetch_feed(name, url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
        items = root.findall(".//item")[:MAX_PER_FEED]
        results = []
        for item in items:
            title = (item.findtext("title") or "").strip()
            link  = (item.findtext("link") or "").strip()
            desc  = (item.findtext("description") or "").strip()[:200]
            pub   = (item.findtext("pubDate") or "").strip()
            results.append({"source": name, "title": title, "link": link, "desc": desc, "pub": pub})
        return results
    except Exception as e:
        print(f"[WARN] {name}: {e}", file=sys.stderr)
        return []


def is_macro(item):
    text = (item["title"] + " " + item["desc"]).lower()
    return any(kw in text for kw in MACRO_KEYWORDS)


def main():
    all_items = []
    for name, url in FEEDS:
        all_items.extend(fetch_feed(name, url))

    sent_links = _load_sent_links()
    new_links  = set()

    # Filter to unseen items only
    fresh_items = [i for i in all_items if not i.get("link") or i["link"] not in sent_links]
    skipped = len(all_items) - len(fresh_items)
    if skipped:
        print(f"[dedup] Skipped {skipped} already-sent item(s).", file=sys.stderr)

    macro_items = [i for i in fresh_items if is_macro(i)]
    other_items = [i for i in fresh_items if not is_macro(i)]

    print(f"=== MACRO / HIGH-IMPACT NEWS ({len(macro_items)} items) ===")
    if macro_items:
        for item in macro_items:
            print(f"\n[{item['source']}] {item['title']}")
            if item["desc"]:
                print(f"  {item['desc'][:150]}...")
            if item["pub"]:
                print(f"  Published: {item['pub']}")
            if item.get("link"):
                new_links.add(item["link"])
    else:
        print("No macro headlines detected in latest feed items.")

    print(f"\n=== OTHER RECENT HEADLINES ({len(other_items)} items) ===")
    for item in other_items[:10]:
        print(f"[{item['source']}] {item['title']}")
        if item.get("link"):
            new_links.add(item["link"])

    print(f"\nFetched at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")

    # Persist seen links
    sent_links.update(new_links)
    _save_sent_links(sent_links)


if __name__ == "__main__":
    main()

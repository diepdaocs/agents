#!/usr/bin/env python3
"""Fetch macro/financial news from public RSS feeds for market-hedge skill."""

import json
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

SENT_CACHE_FILE = os.path.expanduser("~/.openclaw/news_cache/market_hedge_sent_links.json")
SENT_CACHE_MAX  = 2000


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
    # Global macro / finance
    ("Reuters Business",     "https://feeds.reuters.com/reuters/businessNews"),
    ("Reuters Commodities",  "https://feeds.reuters.com/reuters/CommoditiesNews"),
    ("Reuters Markets",      "https://feeds.reuters.com/reuters/companyNews"),
    ("Barrons",              "https://www.barrons.com/feed"),
    ("MarketWatch",          "https://feeds.content.dowjones.io/public/rss/mw_marketpulse"),
    ("CNBC Top News",        "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("FT",                   "https://www.ft.com/world?format=rss"),
    # Google News macro topics
    ("GNews Macro",          "https://news.google.com/rss/search?q=macro+economy+fed+rate+inflation&hl=en-US&gl=US&ceid=US:en"),
    ("GNews Geopolitics",    "https://news.google.com/rss/search?q=geopolitics+war+sanctions+trade&hl=en-US&gl=US&ceid=US:en"),
    ("GNews Commodities",    "https://news.google.com/rss/search?q=oil+gold+commodity+supply+disruption&hl=en-US&gl=US&ceid=US:en"),
    ("GNews Coffee",         "https://news.google.com/rss/search?q=robusta+coffee+futures+vietnam+inventory&hl=en-US&gl=US&ceid=US:en"),
    # Vietnam
    ("VnExpress Finance",    "https://vnexpress.net/rss/kinh-doanh.rss"),
    ("VnExpress Economy",    "https://vnexpress.net/rss/kinh-te.rss"),
    ("CafeF",                "https://cafef.vn/rss/home.rss"),
]

HEADERS = {"User-Agent": "market-hedge-skill/1.0 (macro news fetcher)"}
MAX_PER_FEED = 8


def fetch_feed(name, url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
        items = root.findall(".//item")[:MAX_PER_FEED]
        results = []
        for item in items:
            title = (item.findtext("title") or "").strip()
            link  = (item.findtext("link") or "").strip()
            desc  = (item.findtext("description") or "").strip()[:300]
            pub   = (item.findtext("pubDate") or "").strip()
            results.append({"source": name, "title": title, "link": link, "desc": desc, "pub": pub})
        return results
    except Exception as e:
        print(f"[WARN] {name}: {e}", file=sys.stderr)
        return []


def main():
    all_items = []
    for name, url in FEEDS:
        items = fetch_feed(name, url)
        all_items.extend(items)
        print(f"[INFO] {name}: {len(items)} items", file=sys.stderr)

    sent_links = _load_sent_links()
    new_links  = set()

    fresh_items = [i for i in all_items if not i.get("link") or i["link"] not in sent_links]
    skipped = len(all_items) - len(fresh_items)
    if skipped:
        print(f"[dedup] Skipped {skipped} already-seen item(s).", file=sys.stderr)

    print(f"=== MACRO NEWS FEED — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} ===")
    print(f"Total fresh items: {len(fresh_items)}\n")

    # Group by source
    by_source: dict = {}
    for item in fresh_items:
        by_source.setdefault(item["source"], []).append(item)

    for source, items in by_source.items():
        print(f"\n--- {source} ({len(items)} items) ---")
        for item in items:
            print(f"  • {item['title']}")
            if item["desc"]:
                clean_desc = item["desc"].replace("<![CDATA[", "").replace("]]>", "").strip()
                print(f"    {clean_desc[:200]}")
            if item["pub"]:
                print(f"    [{item['pub']}]")
            if item.get("link"):
                new_links.add(item["link"])

    # Persist seen links
    sent_links.update(new_links)
    _save_sent_links(sent_links)

    print(f"\n=== END OF FEED ===")


if __name__ == "__main__":
    main()

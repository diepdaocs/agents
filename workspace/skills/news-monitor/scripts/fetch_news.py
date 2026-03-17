#!/usr/bin/env python3
"""Fetch news from reputable RSS feeds for 6 topics: tech, AI, finance, blockchain, tennis, soccer."""

import html
import re
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HEADERS = {"User-Agent": "news-monitor-skill/1.0 (personal-agent)"}
MAX_PER_FEED = 12
MAX_PER_TOPIC = 3

# Source credibility tiers for fact-checking display
TIER1_SOURCES = {
    "Reuters", "Reuters Business", "BBC Sport", "BBC Sport Tennis", "BBC Sport Football",
    "BBC News", "ESPN", "ESPN Tennis", "ESPN Soccer", "CNBC", "AP News",
    "Financial Times", "Bloomberg", "Associated Press",
}
TIER2_SOURCES = {
    "TechCrunch", "The Verge", "The Verge AI", "Ars Technica", "Ars Technica AI",
    "Wired", "VentureBeat", "MIT Tech Review", "CoinDesk", "CoinTelegraph",
    "Decrypt", "TheBlock", "The Block", "MarketWatch",
}

TOPICS = {
    "tech": {
        "label": "Tech",
        "emoji": "💻",
        "feeds": [
            ("TechCrunch",   "https://techcrunch.com/feed/"),
            ("The Verge",    "https://www.theverge.com/rss/index.xml"),
            ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
            ("Wired",        "https://www.wired.com/feed/rss"),
        ],
        "keywords": [
            "tech", "software", "hardware", "startup", "app", "gadget", "device",
            "microsoft", "apple", "google", "meta", "amazon", "samsung", "intel",
            "nvidia", "chip", "semiconductor", "cloud", "cybersecurity", "privacy",
            "data", "developer", "open source", "launch", "release", "product",
        ],
        "exclude": ["football", "soccer", "tennis", "basketball", "nfl", "nba",
                    "bitcoin", "ethereum", "crypto", "blockchain"],
    },
    "ai": {
        "label": "Artificial Intelligence",
        "emoji": "🤖",
        "feeds": [
            ("VentureBeat",   "https://venturebeat.com/category/ai/feed/"),
            ("The Verge AI",  "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
            ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
            ("Ars Technica",  "https://feeds.arstechnica.com/arstechnica/index"),
        ],
        "keywords": [
            "artificial intelligence", "machine learning", " ai ", "gpt", "llm",
            "large language", "openai", "anthropic", "deepmind", "gemini", "claude",
            "chatgpt", "neural network", "deep learning", "generative ai",
            "diffusion model", "language model", "foundation model", "ai model",
            "robotics", "automation", "natural language processing",
        ],
        "exclude": ["football", "soccer", "tennis", "bitcoin", "crypto"],
    },
    "finance": {
        "label": "Finance and Markets",
        "emoji": "📈",
        "feeds": [
            ("Reuters Business", "https://feeds.reuters.com/reuters/businessNews"),
            ("CNBC",            "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
            ("MarketWatch",     "https://feeds.content.dowjones.io/public/rss/mw_topstories"),
        ],
        "keywords": [
            "stock", "market", "economy", "gdp", "inflation", "interest rate", "fed ",
            "federal reserve", "bank", "finance", "investment", "earnings", "revenue",
            "recession", "bond", "yield", "dollar", "currency", "ipo", "acquisition",
            "merger", "hedge fund", "wall street", "s&p", "nasdaq", "dow jones",
            "trade war", "tariff", "treasury", "imf", "world bank", "rate hike",
        ],
        "exclude": ["bitcoin", "ethereum", "crypto", "soccer", "football", "tennis"],
    },
    "blockchain": {
        "label": "Blockchain and Crypto",
        "emoji": "⛓️",
        "feeds": [
            ("CoinDesk",     "https://www.coindesk.com/arc/outboundfeeds/rss/"),
            ("CoinTelegraph", "https://cointelegraph.com/rss"),
            ("Decrypt",      "https://decrypt.co/feed"),
            ("TheBlock",     "https://www.theblock.co/rss.xml"),
        ],
        "keywords": [
            "bitcoin", "ethereum", "blockchain", "crypto", "defi", "nft", "web3",
            "solana", "wallet", "token", "protocol", "exchange", "btc", "eth", "sol",
            "stablecoin", "layer 2", "layer2", "dao", "smart contract", "mining",
            "staking", "validator", "halving", "etf", "sec crypto",
        ],
        "exclude": [],
    },
    "tennis": {
        "label": "Tennis — Alcaraz",
        "emoji": "🎾",
        "feeds": [
            ("ESPN Tennis",      "https://www.espn.com/espn/rss/tennis/news"),
            ("BBC Sport Tennis", "https://feeds.bbci.co.uk/sport/tennis/rss.xml"),
        ],
        "keywords": [
            "alcaraz", "carlos alcaraz", "tennis", "atp", "wta", "wimbledon",
            "french open", "us open", "australian open", "roland garros",
            "grand slam", "atp tour", "masters 1000",
        ],
        "exclude": [],
        "require_any": ["alcaraz", "tennis"],
    },
    "soccer": {
        "label": "Soccer — FC Barcelona",
        "emoji": "⚽",
        "feeds": [
            ("ESPN Soccer",        "https://www.espn.com/espn/rss/soccer/news"),
            ("BBC Sport Football", "https://feeds.bbci.co.uk/sport/football/rss.xml"),
        ],
        "keywords": [
            "barcelona", "barca", "fc barcelona", "laliga", "la liga",
            "champions league", "lamine yamal", "lewandowski", "hansi flick",
            "pedri", "gavi", "ter stegen", "raphinha", "dani olmo",
        ],
        "exclude": [],
        "require_any": ["barcelona", "barca"],
    },
}


def _strip_html(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_feed(name, url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
        items = root.findall(".//item")[:MAX_PER_FEED]
        results = []
        for item in items:
            title = _strip_html(item.findtext("title") or "")
            link  = (item.findtext("link") or "").strip()
            desc  = _strip_html(item.findtext("description") or "")[:250]
            pub   = (item.findtext("pubDate") or "").strip()
            if title:
                results.append({"source": name, "title": title, "link": link,
                                 "desc": desc, "pub": pub})
        return results
    except Exception as e:
        print(f"[WARN] {name}: {e}", file=sys.stderr)
        return []


def is_relevant(item, config):
    text = (item["title"] + " " + item["desc"]).lower()

    keywords = config.get("keywords", [])
    if keywords and not any(kw.lower() in text for kw in keywords):
        return False

    require_any = config.get("require_any", [])
    if require_any and not any(kw.lower() in text for kw in require_any):
        return False

    exclude = config.get("exclude", [])
    if any(kw.lower() in text for kw in exclude):
        return False

    return True


def score_item(item, config):
    text = (item["title"] + " " + item["desc"]).lower()
    score = sum(1 for kw in config.get("keywords", []) if kw.lower() in text)
    if item["source"] in TIER1_SOURCES:
        score += 3
    elif item["source"] in TIER2_SOURCES:
        score += 1
    return score


def dedup(items):
    """Remove near-duplicate headlines by title word overlap."""
    seen_words = []
    result = []
    for item in items:
        words = set(w for w in item["title"].lower().split() if len(w) > 3)
        is_dup = False
        for sw in seen_words:
            if words and sw:
                overlap = len(words & sw) / max(len(words | sw), 1)
                if overlap > 0.55:
                    is_dup = True
                    break
        if not is_dup:
            seen_words.append(words)
            result.append(item)
    return result


def credibility_tag(item):
    if item["source"] in TIER1_SOURCES:
        return "✅"
    elif item["source"] in TIER2_SOURCES:
        return "✓"
    return "⚠️"


def fetch_topic(topic_key):
    config = TOPICS[topic_key]
    all_items = []
    for name, url in config["feeds"]:
        all_items.extend(fetch_feed(name, url))

    relevant = [i for i in all_items if is_relevant(i, config)]
    relevant = dedup(relevant)
    relevant.sort(key=lambda i: score_item(i, config), reverse=True)
    return relevant[:MAX_PER_TOPIC]


def fetch_all():
    """Fetch news for all topics. Returns dict of topic_key -> list of items."""
    results = {}
    for topic_key in TOPICS:
        results[topic_key] = fetch_topic(topic_key)
    return results


def format_topic_html(topic_key, items):
    """Format a topic section as Telegram HTML."""
    config = TOPICS[topic_key]
    emoji = config["emoji"]
    label = config["label"]

    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    lines = [f"{emoji} <b>{esc(label)}</b>"]
    if not items:
        lines.append("  No news available.")
    else:
        for item in items:
            tag = credibility_tag(item)
            title = esc(item["title"])
            source = esc(item["source"])
            desc = esc(item["desc"][:120]) if item["desc"] else ""
            lines.append(f"\n• <b>{title}</b>")
            if desc:
                lines.append(f"  {desc}")
            lines.append(f"  <i>{tag} {source}</i>")

    return "\n".join(lines)


if __name__ == "__main__":
    # Standalone test: print all topics
    for topic_key, config in TOPICS.items():
        print(f"\n=== {config['label']} ===")
        items = fetch_topic(topic_key)
        if items:
            for item in items:
                tag = credibility_tag(item)
                print(f"  {tag} [{item['source']}] {item['title']}")
        else:
            print("  No relevant news found.")
    print(f"\nFetched at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")

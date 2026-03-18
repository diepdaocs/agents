#!/usr/bin/env python3
"""Fetch news from reputable RSS feeds for 6 topics: tech, AI, finance, blockchain, tennis, soccer."""

import html
import json
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
    "Reuters", "Reuters Business", "Reuters Commodities",
    "BBC Sport", "BBC Sport Tennis", "BBC Sport Football",
    "BBC News", "ESPN", "ESPN Tennis", "ESPN Soccer", "CNBC", "AP News",
    "Financial Times", "Bloomberg", "Associated Press", "The Economist",
}
TIER2_SOURCES = {
    "TechCrunch", "The Verge", "The Verge AI", "Ars Technica", "Ars Technica AI",
    "Wired", "VentureBeat", "MIT Tech Review", "CoinDesk", "CoinTelegraph",
    "Decrypt", "TheBlock", "The Block", "MarketWatch",
    "Hacker News", "Investing.com", "VnExpress",
    "Barrons", "Goal.com", "FC Barcelona",
    "Google AI Blog", "Google Developers", "Meta Engineering",
    "Microsoft Dev Blog", "OpenAI Blog", "Anthropic Blog",
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
            ("The Economist",  "https://www.economist.com/finance-and-economics/rss.xml"),
            ("Bloomberg",      "https://feeds.bloomberg.com/markets/news.rss"),
            ("Barrons",        "https://www.barrons.com/articles?type=article&format=rss"),
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
    "hackernews": {
        "label": "Hacker News",
        "emoji": "🔶",
        "custom_fetcher": "hackernews",
        "feeds": [],
        "keywords": [],
        "exclude": [],
    },
    "engblogs": {
        "label": "Engineering Blogs",
        "emoji": "🛠️",
        "feeds": [
            ("Google AI Blog",     "https://blog.research.google/feeds/posts/default?alt=rss"),
            ("Google Developers",  "https://developers.googleblog.com/feeds/posts/default?alt=rss"),
            ("Meta Engineering",   "https://engineering.fb.com/feed/"),
            ("Microsoft Dev Blog", "https://devblogs.microsoft.com/engineering-at-microsoft/feed/"),
            ("OpenAI Blog",        "https://openai.com/news/rss.xml"),
        ],
        "keywords": [
            "engineering", "infrastructure", "system", "architecture", "performance",
            "scalability", "reliability", "open source", "research", "paper",
            "model", "training", "deploy", "framework", "api", "sdk",
            "machine learning", "distributed", "database", "compiler", "runtime",
            "security", "benchmark", "optimization", "developer", "platform",
        ],
        "exclude": ["tennis", "soccer", "football", "basketball", "sports"],
    },
    "coffee": {
        "label": "Coffee & Robusta Futures",
        "emoji": "☕",
        "feeds": [
            ("Reuters Commodities", "https://feeds.reuters.com/reuters/commoditiesNews"),
            ("Reuters Business",    "https://feeds.reuters.com/reuters/businessNews"),
            ("Investing.com",       "https://www.investing.com/rss/news_14.rss"),
            ("VnExpress",           "https://e.vnexpress.net/rss/business.rss"),
        ],
        "keywords": [
            "coffee", "robusta", "arabica", "coffee futures", "coffee price",
            "coffee market", "coffee export", "coffee harvest", "coffee crop",
            "vietnam coffee", "brazil coffee", "ice futures", "coffee trading",
            "coffee supply", "coffee demand", "liffe", "coffee bean",
            "coffee production", "coffee stocks", "soft commodities",
        ],
        "exclude": [],
        "require_any": ["coffee", "robusta", "arabica"],
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
            ("Goal.com",           "https://www.goal.com/en/rss"),
            ("FC Barcelona",       "https://www.fcbarcelona.com/en/rss"),
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


_ATOM = "http://www.w3.org/2005/Atom"


def fetch_feed(name, url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
        results = []

        # RSS 2.0
        items = root.findall(".//item")
        if items:
            for item in items[:MAX_PER_FEED]:
                title = _strip_html(item.findtext("title") or "")
                link  = (item.findtext("link") or "").strip()
                desc  = _strip_html(item.findtext("description") or "")[:250]
                pub   = (item.findtext("pubDate") or "").strip()
                if title:
                    results.append({"source": name, "title": title, "link": link,
                                     "desc": desc, "pub": pub})
            return results

        # Atom
        entries = root.findall(f"{{{_ATOM}}}entry")
        for entry in entries[:MAX_PER_FEED]:
            title = _strip_html(entry.findtext(f"{{{_ATOM}}}title") or "")
            link_el = entry.find(f"{{{_ATOM}}}link[@rel='alternate']") or entry.find(f"{{{_ATOM}}}link")
            link  = (link_el.get("href") if link_el is not None else "")
            desc  = _strip_html(
                entry.findtext(f"{{{_ATOM}}}summary") or
                entry.findtext(f"{{{_ATOM}}}content") or ""
            )[:250]
            pub   = (entry.findtext(f"{{{_ATOM}}}published") or
                     entry.findtext(f"{{{_ATOM}}}updated") or "").strip()
            if title:
                results.append({"source": name, "title": title, "link": link,
                                 "desc": desc, "pub": pub})
        return results

    except Exception as e:
        print(f"[WARN] {name}: {e}", file=sys.stderr)
        return []


def _fetch_hn_comments(story_id, max_comments=2):
    """Fetch top-level comments for a HN story via Algolia items API."""
    url = f"https://hn.algolia.com/api/v1/items/{story_id}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        comments = []
        for child in (data.get("children") or []):
            text = _strip_html(child.get("text") or "").strip()
            # Remove raw URLs to keep comment text clean in Telegram
            text = re.sub(r"https?://\S+", "", text).strip()
            author = child.get("author") or ""
            if text and author and len(text) > 20:
                comments.append({"author": author, "text": text[:180]})
            if len(comments) >= max_comments:
                break
        return comments
    except Exception:
        return []


def fetch_hn_top(max_items=10):
    """Fetch top HN stories with article summary and top comments."""
    url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read())
        results = []
        for hit in data.get("hits", [])[:max_items]:
            title = (hit.get("title") or "").strip()
            story_id = hit.get("objectID", "")
            points = hit.get("points") or 0
            num_comments = hit.get("num_comments") or 0
            hn_url = f"https://news.ycombinator.com/item?id={story_id}"
            # story_text exists for Ask HN / Show HN posts
            story_text = _strip_html(hit.get("story_text") or "")[:200].strip()
            if title:
                results.append({
                    "source": "Hacker News",
                    "title": title,
                    "link": hn_url,
                    "desc": f"▲ {points} pts · {num_comments} comments",
                    "pub": "",
                    "hn_url": hn_url,
                    "hn_story_text": story_text,
                    "hn_story_id": story_id,
                })
        # Fetch comments only for the top MAX_PER_TOPIC stories (avoid slow requests)
        for item in results[:MAX_PER_TOPIC]:
            item["hn_comments"] = _fetch_hn_comments(item["hn_story_id"])
        return results
    except Exception as e:
        print(f"[WARN] HackerNews: {e}", file=sys.stderr)
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

    if config.get("custom_fetcher") == "hackernews":
        items = fetch_hn_top(MAX_PER_FEED)
        items = dedup(items)
        return items[:MAX_PER_TOPIC]

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
            link = item.get("link", "").strip()
            title_html = f'<a href="{link}">{title}</a>' if link else title
            lines.append(f"\n• <b>{title_html}</b>")
            if desc:
                lines.append(f"  {desc}")
            # HN story body (Ask HN / Show HN posts)
            story_text = item.get("hn_story_text", "")
            if story_text:
                lines.append(f"  <i>{esc(story_text[:150])}</i>")
            # HN top comments
            for c in item.get("hn_comments", []):
                lines.append(f"  💬 <b>{esc(c['author'])}</b>: {esc(c['text'])}")
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

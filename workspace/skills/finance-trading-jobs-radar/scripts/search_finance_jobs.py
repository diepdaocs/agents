#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import List

import requests

TIMEOUT = 25
UA = {"User-Agent": "Mozilla/5.0 (OpenClaw finance-trading-jobs-radar)"}
DEFAULT_LOCATION = "singapore"
DEFAULT_LIMIT = 12
MAX_PER_COMPANY = 2

GREENHOUSE_BOARDS = [
    "janestreet",
    "jumptrading",
    "flowtraders",
    "imc",
    "virtu",
    "maven",
    "point72",
    "coinbase",
    "okx",
]

BOARD_BONUS = {
    "janestreet": 18,
    "jumptrading": 18,
    "flowtraders": 16,
    "imc": 16,
    "virtu": 16,
    "maven": 14,
    "point72": 14,
    "coinbase": 8,
    "okx": 6,
}

NEGATIVE = [
    "intern", "recruiter", "sales", "account executive", "customer success",
    "business development", "marketing", "legal", "compliance analyst", "mobile",
    "android", "ios", "designer", "support specialist", "analyst", "product manager",
    "technical product manager", "program manager",
]

POSITIVE = [
    "staff", "principal", "lead", "senior", "backend", "back-end", "platform",
    "data", "infrastructure", "software engineer", "distributed", "java", "python",
    "trading", "risk", "market", "low latency", "ml", "ai", "machine learning",
]

@dataclass
class Job:
    company: str
    title: str
    location: str
    url: str
    source: str
    summary: str
    score: int


def strip_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def score_job(company: str, title: str, location: str, summary: str, target_location: str) -> int:
    text = f"{title} {location} {summary}".lower()
    score = BOARD_BONUS.get(company.lower(), 0)
    if target_location.lower() in text or "singapore" in text or "apac" in text:
        score += 20
    if any(k in text for k in ["staff", "principal", "lead"]):
        score += 10
    for kw in POSITIVE:
        if kw in text:
            score += 5
    for kw in NEGATIVE:
        if kw in text:
            score -= 12
    return score


def fetch_greenhouse(board: str, target_location: str) -> List[Job]:
    url = f"https://api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    r = requests.get(url, headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    payload = r.json().get("jobs", [])
    jobs: List[Job] = []
    for item in payload:
        title = item.get("title", "")
        location = (item.get("location") or {}).get("name", "")
        summary = strip_html(item.get("content", ""))[:500]
        apply_url = item.get("absolute_url")
        jobs.append(Job(
            company=board,
            title=title,
            location=location,
            url=apply_url,
            source=f"greenhouse:{board}",
            summary=summary,
            score=score_job(board, title, location, summary, target_location),
        ))
    return jobs


def is_relevant(job: Job, target_location: str) -> bool:
    text = f"{job.title} {job.location} {job.summary}".lower()
    loc = (job.location or "").lower()
    if not job.url:
        return False
    title = (job.title or "").lower()
    if not any(k in title for k in ["engineer", "platform", "backend", "software", "infrastructure", "data"]):
        return False
    if any(k in text for k in NEGATIVE):
        return False
    if target_location.lower() not in loc and "singapore" not in loc and "remote - singapore" not in loc and "apac" not in loc:
        return False
    return True


def collect_jobs(location: str) -> List[Job]:
    jobs: List[Job] = []
    for board in GREENHOUSE_BOARDS:
        try:
            jobs.extend(fetch_greenhouse(board, location))
        except Exception:
            continue
    return jobs


def filter_jobs(jobs: List[Job], limit: int, target_location: str) -> List[Job]:
    seen = set()
    filtered: List[Job] = []
    for job in sorted(jobs, key=lambda j: j.score, reverse=True):
        key = (job.company.lower(), job.title.lower(), job.url)
        if key in seen or not is_relevant(job, target_location):
            continue
        seen.add(key)
        filtered.append(job)

    out: List[Job] = []
    counts = defaultdict(int)
    for job in filtered:
        if counts[job.company.lower()] >= MAX_PER_COMPANY:
            continue
        out.append(job)
        counts[job.company.lower()] += 1
        if len(out) >= limit:
            break
    return out


def to_markdown(jobs: List[Job]) -> str:
    lines = []
    for i, job in enumerate(jobs, start=1):
        lines.append(f"{i}. **{job.title}** — {job.company}")
        lines.append(f"   - Location: {job.location}")
        lines.append(f"   - Score: {job.score}")
        lines.append(f"   - Apply: {job.url}")
        lines.append(f"   - Source: {job.source}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Search direct public ATS feeds for finance/trading engineering jobs.")
    ap.add_argument("--location", default=DEFAULT_LOCATION)
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    jobs = filter_jobs(collect_jobs(args.location), args.limit, args.location)
    if args.json:
        print(json.dumps([asdict(j) for j in jobs], indent=2))
    else:
        print(to_markdown(jobs))
    return 0


if __name__ == "__main__":
    sys.exit(main())

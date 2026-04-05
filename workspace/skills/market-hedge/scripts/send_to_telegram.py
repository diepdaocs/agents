#!/usr/bin/env python3
"""Send the saved market hedge report to Telegram."""

import json
import os
import sys
import urllib.request

TELEGRAM_BOT_TOKEN = "8625186050:AAGJ-BfSs3v4intvZCg7bH3fGE2SIV-oHcA"
TELEGRAM_CHAT_ID   = "6202550149"
TELEGRAM_API       = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
REPORT_PATH        = os.path.expanduser("~/code/agents/workspace/market_hedge_report.txt")
MAX_CHUNK          = 3500


def send_telegram(text):
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }).encode("utf-8")
    req = urllib.request.Request(
        TELEGRAM_API, data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read())


def split_chunks(text, max_len=MAX_CHUNK):
    """Split text into chunks at newline boundaries."""
    chunks = []
    current = []
    current_len = 0
    for line in text.splitlines(keepends=True):
        if current_len + len(line) > max_len and current:
            chunks.append("".join(current))
            current = []
            current_len = 0
        current.append(line)
        current_len += len(line)
    if current:
        chunks.append("".join(current))
    return chunks


def main():
    if not os.path.exists(REPORT_PATH):
        print(f"Report not found: {REPORT_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(REPORT_PATH, "r") as f:
        report = f.read().strip()

    if not report:
        print("Report is empty.", file=sys.stderr)
        sys.exit(1)

    chunks = split_chunks(report)
    for i, chunk in enumerate(chunks, 1):
        print(f"Sending chunk {i}/{len(chunks)} ({len(chunk)} chars)...")
        result = send_telegram(chunk)
        if not result.get("ok"):
            print(f"Telegram error: {result}", file=sys.stderr)
            sys.exit(1)

    print(f"Sent {len(chunks)} message(s) to Telegram.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fetch current prices, 24h/7d changes, volatility, and Fear & Greed index for BTC, ETH, SOL."""

import json
import math
import sys
import urllib.request
import urllib.error

COINGECKO = "https://api.coingecko.com/api/v3"
HEADERS = {"User-Agent": "crypto-monitor-skill/1.0"}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def main():
    # --- Prices ---
    try:
        prices = fetch(
            f"{COINGECKO}/simple/price"
            "?ids=bitcoin,ethereum,solana"
            "&vs_currencies=usd"
            "&include_24hr_change=true"
            "&include_7d_change=true"
            "&include_market_cap=true"
        )
        print("=== PORTFOLIO PRICES ===")
        mapping = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana"}
        for symbol, coin_id in mapping.items():
            d = prices.get(coin_id, {})
            price  = d.get("usd", "N/A")
            chg24  = d.get("usd_24h_change") or 0
            chg7d  = d.get("usd_7d_change") or 0
            mcap   = d.get("usd_market_cap") or 0
            alert  = " ⚠️" if abs(chg24) >= 5 else ""
            print(
                f"{symbol}: ${price:,.2f}  |  "
                f"24h: {chg24:+.2f}%  |  "
                f"7d: {chg7d:+.2f}%  |  "
                f"MCap: ${mcap/1e9:.1f}B{alert}"
            )
    except Exception as e:
        print(f"[ERROR] Prices: {e}", file=sys.stderr)

    # --- Fear & Greed ---
    print("\n=== FEAR & GREED INDEX ===")
    try:
        fng = fetch("https://api.alternative.me/fng/?limit=1")
        entry = fng["data"][0]
        value = int(entry["value"])
        label = entry["value_classification"]
        bar   = "█" * (value // 10) + "░" * (10 - value // 10)
        print(f"{value}/100  [{bar}]  {label}")
    except Exception as e:
        print(f"[ERROR] Fear & Greed: {e}", file=sys.stderr)

    # --- BTC Volatility (7-day OHLC) ---
    print("\n=== VOLATILITY SNAPSHOT (BTC 7-day OHLC) ===")
    try:
        ohlc = fetch(f"{COINGECKO}/coins/bitcoin/ohlc?vs_currency=usd&days=7")
        closes = [c[4] for c in ohlc]
        highs  = [c[2] for c in ohlc]
        lows   = [c[3] for c in ohlc]
        mean   = sum(closes) / len(closes)
        std    = math.sqrt(sum((x - mean) ** 2 for x in closes) / len(closes))
        pct    = (std / mean) * 100
        spread = ((max(highs) - min(lows)) / min(lows)) * 100
        vol_label = (
            "LOW" if pct < 2 else
            "MODERATE" if pct < 5 else
            "HIGH" if pct < 10 else
            "EXTREME"
        )
        print(
            f"7d High: ${max(highs):,.0f}  |  "
            f"7d Low: ${min(lows):,.0f}  |  "
            f"Range: {spread:.1f}%  |  "
            f"Std Dev: {pct:.2f}%  →  {vol_label} VOLATILITY"
        )
    except Exception as e:
        print(f"[ERROR] Volatility: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

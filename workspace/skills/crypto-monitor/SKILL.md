---
name: crypto-monitor
description: "Monitor BTC, ETH, SOL portfolio. Alert via Telegram on macro/radical news that could move portfolio 10%+. Provide hedging strategies using futures/options based on volatility. Use when asked to check crypto portfolio, monitor markets, or assess macro crypto risk."
metadata:
  {
    "openclaw":
      {
        "emoji": "₿",
        "requires": { "bins": ["python3"] },
      },
  }
---

# Crypto Portfolio Monitor

Monitors BTC, ETH, and SOL. Alerts the user via Telegram when macro or radical news could cause a 10%+ portfolio move. Provides hedging strategies tailored to current volatility.

## Portfolio

| Asset | Value (USD) | Notes |
|-------|-------------|-------|
| BTC   | ~$2,000     | ~0.027 BTC at time of setup |
| ETH   | ~$2,000     | ~0.86 ETH at time of setup |
| SOL   | ~$2,000     | ~21.4 SOL at time of setup |
| **Total** | **~$6,000** | Equal-weighted across 3 assets |

> A 10% portfolio move = ~$600 swing. Alert threshold is set accordingly.

## Execution Steps

### 1. Fetch market data
Run the portfolio script to get current prices, 24h/7d changes, and volatility:
```bash
python3 ~/code/agents/workspace/skills/crypto-monitor/scripts/fetch_portfolio.py
```

### 2. Fetch news
Run the news script to pull latest RSS headlines from CoinDesk, CoinTelegraph, Decrypt, and TheBlock:
```bash
python3 ~/code/agents/workspace/skills/crypto-monitor/scripts/fetch_news.py
```

### 3. Calculate current portfolio value
Use live prices from step 1 to estimate current total value:
- BTC value = live BTC price × 0.027
- ETH value = live ETH price × 0.86
- SOL value = live SOL price × 21.4
- Total and compare to $6,000 baseline

### 4. Assess macro impact
Analyze the news output. Focus on:
- **Macro events**: Fed rate decisions, CPI/inflation data, GDP, geopolitical events, war/sanctions
- **Regulatory**: SEC actions, ETF approvals/rejections, country bans, Congressional hearings
- **Institutional**: Major fund inflows/outflows, Blackrock/Fidelity moves, sovereign adoption
- **Radical/Black swan**: Exchange hacks, major stablecoin depegs, protocol exploits, whale liquidations, key protocol forks

### 5. Alert threshold
Only send a Telegram alert if you assess **≥50% probability** that a news event could move the portfolio by **±$600 or more** (±10% of ~$6,000) within 24–72 hours.

Send via:
```bash
openclaw sessions send --message "YOUR_ALERT" --session-key "telegram:6202550149"
```

### 6. Alert message format
```
🚨 CRYPTO ALERT — [Event Type]

📰 Event: [1-2 sentence summary]
🎯 Impact: [Which coins affected and estimated % move]
📊 Direction: [Bullish / Bearish / Uncertain]

📈 Portfolio Snapshot:
  BTC: $X  (24h: X%)  →  ~$X value
  ETH: $X  (24h: X%)  →  ~$X value
  SOL: $X  (24h: X%)  →  ~$X value
  Total: ~$X  (baseline: $6,000)
  Fear & Greed: X/100

🛡️ Hedging Strategies:

[CONSERVATIVE]
• [Strategy 1]
• [Strategy 2]

[MODERATE]
• [Strategy]

[AGGRESSIVE]
• [Strategy]

⚡ Volatility: [LOW/MODERATE/HIGH/EXTREME] (7d std dev: X%)
```

## Hedging Strategy Guidelines

### Bearish macro (rate hike, ban, hack)
- **Conservative**: Buy OTM puts on BTC/ETH (Deribit), 5–10% of portfolio notional (~$300–$600). Or reduce spot 20–30%.
- **Moderate**: Short BTC/ETH perp futures (1–2x), hedging 30–50% of notional. Use tight stop at 5%.
- **Aggressive**: Full short perp, or buy put spreads (buy ATM put, sell OTM put).

### Bullish macro (ETF approval, Fed pivot, institutional buy)
- **Conservative**: Add covered calls on existing holdings to generate yield.
- **Moderate**: Long BTC/ETH/SOL perp futures with 1.5–2x leverage on 20–30% of notional (~$1,200–$1,800).
- **Aggressive**: Call options (ATM or slightly OTM), 1–2 week expiry on Deribit.

### High uncertainty / volatile
- **Straddle**: Buy both ATM call and put — captures large moves either way.
- **Strangle**: Buy OTM call + OTM put for cheaper premium, needs bigger move to profit.
- **Reduce exposure**: Move 20–40% (~$1,200–$2,400) to stablecoins (USDC/USDT) until clarity.

### Low volatility / no clear catalyst
- **Covered calls**: Sell OTM calls (10–15% above spot) to generate 1–3% monthly yield.
- **Cash-secured puts**: Sell OTM puts to accumulate at lower prices with premium income.

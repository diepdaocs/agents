---
name: crypto-monitor
description: Monitor BTC, ETH, SOL portfolio. Alert via Telegram on macro/radical news that could move portfolio 10%+. Provide hedging strategies using futures/options based on volatility. Use when asked to check crypto portfolio, monitor markets, or assess macro crypto risk.
metadata: {"openclaw": {"emoji": "₿", "requires": {"bins": ["python3"]}}}
---

# Crypto Portfolio Monitor

Monitors BTC, ETH, and SOL. Alerts the user via Telegram when macro or radical news could cause a 10%+ portfolio move. Provides hedging strategies tailored to current volatility.

## Portfolio

| Asset | Coins held | Notes |
|-------|-----------|-------|
| BTC   | —         | Update with actual holdings |
| ETH   | —         | Update with actual holdings |
| SOL   | —         | Update with actual holdings |

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

### 3. Assess macro impact
Analyze the news output. Focus on:
- **Macro events**: Fed rate decisions, CPI/inflation data, GDP, geopolitical events, war/sanctions
- **Regulatory**: SEC actions, ETF approvals/rejections, country bans, Congressional hearings
- **Institutional**: Major fund inflows/outflows, Blackrock/Fidelity moves, sovereign adoption
- **Radical/Black swan**: Exchange hacks, major stablecoin depegs, protocol exploits, whale liquidations, key protocol forks

### 4. Alert threshold
Only send a Telegram alert if you assess **≥50% probability** that a news event could move the portfolio by **±10% or more** within 24–72 hours.

If threshold is met, send via:
```bash
openclaw sessions send --message "YOUR_ALERT" --session-key "telegram:6202550149"
```

### 5. Alert message format
Structure the Telegram alert as:

```
🚨 CRYPTO ALERT — [Event Type]

📰 Event: [1-2 sentence summary]
🎯 Impact: [Which coins affected and estimated % move]
📊 Direction: [Bullish / Bearish / Uncertain]

📈 Portfolio Snapshot:
  BTC: $X  (24h: X%)
  ETH: $X  (24h: X%)
  SOL: $X  (24h: X%)
  Fear & Greed: X/100

🛡️ Hedging Strategies:

[CONSERVATIVE]
• [Strategy 1 — e.g., buy BTC put options at X strike]
• [Strategy 2 — e.g., reduce spot exposure by X%]

[MODERATE]
• [Strategy — e.g., short BTC perpetual futures with X% of portfolio notional]
• [Options play — e.g., BTC put spread]

[AGGRESSIVE]
• [Strategy — e.g., full short via futures, 2x leverage]

⚡ Volatility: [LOW/MODERATE/HIGH/EXTREME] (7d std dev: X%)
```

## Hedging Strategy Guidelines

Apply these based on volatility level and news direction:

### Bearish macro (e.g., rate hike, ban, hack)
- **Conservative**: Buy OTM puts (BTC/ETH on Deribit), 5–10% portfolio notional. Or reduce spot 20–30%.
- **Moderate**: Short BTC/ETH perp futures (1–2x), hedging 30–50% of notional exposure. Use tight stop at 5%.
- **Aggressive**: Full short perp, or buy put spreads (buy ATM put, sell OTM put to reduce premium).

### Bullish macro (e.g., ETF approval, Fed pivot, institutional buy)
- **Conservative**: Add covered calls on existing holdings to generate yield while capping upside.
- **Moderate**: Long BTC/ETH/SOL perp futures with 1.5–2x leverage on 20–30% of notional.
- **Aggressive**: Call options (ATM or slightly OTM), 1–2 week expiry on Deribit.

### High uncertainty / volatile
- **Straddle**: Buy both ATM call and put (expensive but captures large moves either way).
- **Strangle**: Buy OTM call + OTM put for cheaper premium, needs bigger move to profit.
- **Reduce overall exposure**: Move 20–40% to stablecoins (USDC/USDT) until clarity.

### Low volatility / no clear catalyst
- **Covered calls**: Sell OTM calls (10–15% above spot) to generate 1–3% monthly yield.
- **Cash-secured puts**: Sell OTM puts to accumulate at lower prices with premium income.

## Cron Schedule

This skill is designed to run every 4 hours via:
```bash
openclaw cron add --name crypto-monitor --cron "0 */4 * * *" --message "Run the crypto-monitor skill: fetch portfolio data and news, assess macro impact, and send a Telegram alert if any news could move the portfolio by 10% or more. Include hedging strategies."
```

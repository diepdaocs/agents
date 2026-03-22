---
name: market-hedge
description: "Daily macro hedging strategy report. Fetches news from Reuters, Barron's, CNBC, FT, VnExpress, CafeF, Google News. Analyzes geopolitics, inflation, supply shocks, and commodity signals to generate actionable hedging strategies across equities, commodities, rates, and crypto. Sends to Telegram. Use when asked for hedging strategies, macro hedge report, or daily market hedge."
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["python3"] },
      },
  }
---

# Market Hedge — Daily Macro Hedging Strategies

Fetches macro and financial news, then generates actionable hedging strategies as a global macro hedge fund strategist.

## Execution Steps

### 1. Fetch macro news

```bash
python3 ~/code/agents/workspace/skills/market-hedge/scripts/fetch_macro_news.py
```

### 2. Analyze and generate hedging strategies

You are a global macro hedge fund strategist.

Your task is to generate actionable hedging strategies based on major geopolitical and macroeconomic events.

## OBJECTIVE
Identify macro risks and propose hedging strategies across:
- Commodities (oil, gas, gold, agriculture, coffee/robusta)
- Equity indices (S&P 500, Nasdaq, China, Vietnam VNIndex)
- Rates / inflation proxies (if relevant)
- Crypto (BTC, ETH as risk proxy, NOT safe haven by default)

---

## INPUT SOURCES

Use the news output from step 1, sourced from:

1. NEWS (last 24h, high quality only):
- Reuters
- Bloomberg
- The Economist
- Barron's
- Financial Times
- Google News aggregation

2. VIETNAM SOURCES:
- Cafef
- VN Economy
- Local macro / policy / banking / export news

3. COMMODITY DATA:
- Coffee (Robusta) inventory, supply, weather, export data
- Energy supply disruptions
- Agricultural flows (wheat, fertilizer)

---

## ANALYSIS FRAMEWORK

Step 1: Identify major macro events
- War / escalation (e.g. US–Iran, China–Taiwan)
- Inflation / central bank shifts
- Supply chain disruption
- Sanctions / trade wars
- Liquidity shocks

Step 2: Map to historical analogs
- Compare with past events (e.g. Russia–Ukraine war, COVID shock)
- Identify repeating patterns:
  - Energy spike → inflation → equity drawdown
  - Supply shock → agri commodities spike
  - Risk-off → gold up, yields down

Step 3: Transmission channels
- Commodities
- FX / rates
- Equity sectors
- Crypto risk sentiment

Step 4: Generate hedge strategies

For EACH strategy include:
- Trade idea (clear positioning)
- Instruments (futures / ETF proxies)
- Direction (long/short)
- Time horizon (short-term shock / medium-term trend)
- Trigger condition (what must happen)
- Invalidating condition

---

## SPECIAL FOCUS

### Coffee (Robusta trader mode)
- Track:
  - Vietnam exports
  - Inventory levels
  - Weather (Brazil, Vietnam)
- Output specific hedge ideas on robusta futures

---

## OUTPUT FORMAT

### 1. MACRO SUMMARY (3–5 bullets)

### 2. KEY THEMES
- Geopolitics
- Inflation
- Liquidity
- Supply shocks

### 3. HEDGING STRATEGIES

For each:

[Strategy Name]

- Thesis:
- Historical Analog:
- Trade:
- Instruments:
- Timeframe:
- Trigger:
- Risk / Invalidation:

---

### 4. VIETNAM IMPACT
- VNIndex
- FX (VND)
- Exports (coffee, manufacturing)

---

### 5. COFFEE (ROBUSTA) PLAYBOOK
- Inventory signal
- Weather signal
- Trade idea

---

### 6. CONFIDENCE LEVEL
- High / Medium / Low
- Why

---

## STYLE
- Be concise but sharp
- No generic explanations
- Think like a hedge fund PM, not a journalist

### 3. Send to Telegram

Send the full report via:

```bash
openclaw sessions send --message "YOUR_REPORT" --session-key "telegram:6202550149"
```

**IMPORTANT: Telegram formatting rules**
- Keep each field on its own line
- Use SHORT, punchy sentences — max 1 line per field
- No prose paragraphs — scannable bullets only
- Split into multiple `openclaw sessions send` calls if total length > 3500 chars
- Use Telegram markdown: *bold* for headers, `code` for instrument tickers

Use this exact message format (3 separate messages):

**Message 1 — Summary + Themes**
```
🛡️ *MACRO HEDGE — [DATE]*

📊 *SUMMARY*
• [1-line bullet]
• [1-line bullet]
• [1-line bullet]

🔑 *KEY THEMES*
🌍 Geo: [1 line]
📈 Inflation: [1 line]
💧 Liquidity: [1 line]
🚢 Supply: [1 line]
```

**Message 2 — Hedging Strategies (one block per strategy)**
```
⚔️ *HEDGING STRATEGIES*

*[Strategy Name]*
↳ Thesis: [1 line]
↳ Analog: [past event]
↳ Trade: LONG/SHORT [asset]
↳ Via: `[TICKER]` / [ETF name]
↳ Horizon: [e.g. 0–3 months]
↳ Trigger: [specific condition]
↳ Kills trade if: [invalidation]

*[Strategy Name]*
↳ ...
```

**Message 3 — Vietnam + Coffee + Confidence**
```
🇻🇳 *VIETNAM*
• VNIndex: [1 line]
• VND: [1 line]
• Exports: [1 line]

☕ *ROBUSTA PLAYBOOK*
• Inventory: [signal]
• Weather: [signal]
• Trade: LONG/SHORT `RK` — [reason]
• Trigger: [specific condition]

🎯 *CONFIDENCE: [HIGH/MEDIUM/LOW]*
[1-line reason]
```

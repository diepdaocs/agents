#!/bin/bash

# Crypto Monitor — fetches prices for top coins via CoinGecko public API
# Usage: ./monitor_crypto.sh [coin1,coin2,...] [currency]
# Defaults: BTC, ETH, SOL, BNB in USD

COINS="${1:-bitcoin,ethereum,solana,binancecoin}"
CURRENCY="${2:-usd}"

RESPONSE=$(curl -sf "https://api.coingecko.com/api/v3/simple/price?ids=${COINS}&vs_currencies=${CURRENCY}&include_24hr_change=true")

if [ -z "$RESPONSE" ]; then
    echo "❌ Failed to fetch crypto prices."
    exit 1
fi

echo "📈 Crypto Prices (${CURRENCY^^}) — $(date '+%Y-%m-%d %H:%M')"
echo ""

# Parse and display each coin
echo "$RESPONSE" | python3 -c "
import sys, json

data = json.load(sys.stdin)
currency = '${CURRENCY}'
symbols = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'solana': 'SOL',
    'binancecoin': 'BNB',
}

for coin, values in data.items():
    symbol = symbols.get(coin, coin.upper())
    price = values.get(currency, 'N/A')
    change = values.get(f'{currency}_24h_change', None)
    if isinstance(price, float) and price >= 1:
        price_fmt = f'\${price:,.2f}'
    else:
        price_fmt = f'\${price}'
    if change is not None:
        arrow = '🟢' if change >= 0 else '🔴'
        print(f'  {arrow} {symbol}: {price_fmt}  ({change:+.2f}% 24h)')
    else:
        print(f'  {symbol}: {price_fmt}')
"

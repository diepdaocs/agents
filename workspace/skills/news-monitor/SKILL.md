# News Monitor Skill

## Purpose
Monitor official news in 6 topics: tech, AI, finance, blockchain, tennis (Alcaraz), soccer (Barcelona). Deliver curated summaries to Telegram at 7:30 AM, 1 PM, 7 PM, and 10 PM SGT.

## Topics
- Tech: Hardware, software, startups, gadgets
- AI: Research, models, applications, ethics
- Finance: Markets, economy, banking, fintech
- Blockchain: Crypto, DeFi, NFTs, Web3
- Tennis: Carlos Alcaraz tournament results, news
- Soccer: FC Barcelona matches, transfers, news

## Sources
Use only reputable sources (Financial Times, The Economist, Bloomberg, Barron's, Reuters, TechCrunch, The Verge, CoinDesk, ESPN, etc.). Perform fact-checking before inclusion.

## Delivery Schedule
- 7:30 AM SGT (daily)
- 1:00 PM SGT (daily)
- 7:00 PM SGT (daily)
- 10:00 PM SGT (daily)

## Output Format
Telegram message with:
- Topic headings
- 2-3 key headlines per topic
- Brief summary (1-2 sentences)
- Source attribution
- Fact-check indicator

## Fact-Checking
Cross-reference news across multiple reputable sources before inclusion. Flag unverified claims.

## Dependencies
- web_search: For news discovery
- web_fetch: For article content extraction
- Telegram API: For delivery

## Configuration
Update topics/specific interests in this file as needed.
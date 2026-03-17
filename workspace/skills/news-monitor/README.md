# News Monitor Skill

## Overview
Automated news monitoring and delivery system for 6 topics: tech, AI, finance, blockchain, tennis (Carlos Alcaraz), and soccer (FC Barcelona).

## Features
- Fact-checked news from reputable sources
- Scheduled delivery at 7:30 AM, 1 PM, 7 PM, and 10 PM SGT
- Telegram integration
- Multiple source verification

## Quick Setup
1. Configure Telegram bot in send-telegram.sh
2. Set up cron jobs from cron-jobs.md
3. Test with: `./scripts/fetch-and-send.sh test`

## Topics Covered
- Technology
- Artificial Intelligence  
- Finance & Markets
- Blockchain & Crypto
- Tennis (Carlos Alcaraz)
- Soccer (FC Barcelona)

## Fact-Checking
All news is cross-referenced across multiple reputable sources before delivery.
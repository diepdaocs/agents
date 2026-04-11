# News Monitor Skill

## Overview
Automated news monitoring and delivery system that fetches source URLs, summarizes the top link per topic, and explains why it matters.

## Features
- Fact-checked news from reputable sources
- Scheduled delivery at 7:00 AM and 7:00 PM SGT
- Telegram integration
- Fetches the source pages for shortlisted links before summarizing
- Why-it-matters note for each top link

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
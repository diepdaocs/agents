#!/bin/bash

# Test the news monitor setup

echo "Testing news monitor setup..."

# Check if scripts exist
if [[ -f "scripts/fetch-news.sh" ]]; then
    echo "✓ fetch-news.sh exists"
else
    echo "✗ fetch-news.sh missing"
fi

if [[ -f "scripts/send-telegram.sh" ]]; then
    echo "✓ send-telegram.sh exists"
else
    echo "✗ send-telegram.sh missing"
fi

if [[ -f "scripts/fetch-and-send.sh" ]]; then
    echo "✓ fetch-and-send.sh exists"
else
    echo "✗ fetch-and-send.sh missing"
fi

echo ""
echo "Setup complete. Next steps:"
echo "1. Configure Telegram bot in send-telegram.sh"
echo "2. Set up cron jobs from cron-jobs.md"
echo "3. Test with: ./scripts/fetch-and-send.sh test"
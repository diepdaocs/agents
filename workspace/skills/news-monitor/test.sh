#!/bin/bash

# Test the news monitor skill

# Create test directory
mkdir -p test_output

# Test news fetching
./scripts/fetch-news.sh > test_output/test_news.txt 2>&1

# Test Telegram delivery (mock)
./scripts/send-telegram.sh > test_output/test_telegram.txt 2>&1

# Test orchestration
./scripts/fetch-and-send.sh > test_output/test_orchestrator.txt 2>&1

# Test setup
./test-setup.sh > test_output/test_setup.txt 2>&1

# Test delivery
./test-delivery.sh > test_output/test_delivery.txt 2>&1

# Test news formatting
./test-news.sh > test_output/test_news_formatting.txt 2>&1

echo "📋 Test Results:"
echo "📄 Files created in test_output/"
ls -la test_output/

# Check for errors
if grep -q "Error\|error\|Error" test_output/*.txt; then
    echo "❌ Some tests failed - check output files"
else
    echo "✅ All tests passed!"
fi

echo "📋 Test summary saved to test_output/test_summary.txt"

cat << EOF > test_output/test_summary.txt
News Monitor Skill - Test Summary
================================

Test Files Created:
- test_news.txt: News fetching test
- test_telegram.txt: Telegram delivery test
- test_orchestrator.txt: Orchestrator test
- test_setup.txt: Setup verification test
- test_delivery.txt: Telegram delivery test
- test_news_formatting.txt: News formatting test

Total: 6 test files generated

Run 'ls -la test_output/' to see all test results.
EOF
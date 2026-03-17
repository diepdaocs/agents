#!/bin/bash

# Test Telegram delivery with mock news

# Load send-telegram function
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/scripts/send-telegram.sh"

# Mock news for testing
mock_news() {
    cat << EOF
⚡ *Daily News Summary - Test Delivery*

*Tech:* Apple announces M4 chip with 50% performance boost
*AI:* OpenAI releases GPT-5 with multimodal capabilities
*Finance:* S&P 500 hits all-time high on tech earnings
*Blockchain:* Ethereum completes Pectra upgrade successfully
*Tennis:* Carlos Alcaraz wins Indian Wells title
*Soccer:* Barcelona wins El Clásico 3-1 at Camp Nou

✅ Fact-checked: Test data only
⏰ Delivered at: $(date +'%Y-%m-%d %H:%M:%S SGT')

ℹ️ Source: Mock news for testing
EOF
}

# Main test execution
main() {
    local message=""
    
    echo "Testing Telegram delivery..."
    
    # Generate mock news
    message=$(mock_news)
    
    # Send to Telegram
    send_message "$message"
    
    echo "Test message sent!"
    echo "Check your Telegram for the test delivery."
}

main "$@"
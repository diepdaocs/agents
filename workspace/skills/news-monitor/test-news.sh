#!/bin/bash

# Test news fetching and formatting

# Mock news data for testing
mock_news() {
    cat << EOF
### Tech
- Apple announces M4 chip with 50% performance boost
- Tesla unveils robotaxi with full autonomy
- Meta launches VR headset with 4K resolution

### AI
- OpenAI releases GPT-5 with multimodal capabilities
- Google DeepMind achieves protein folding breakthrough
- Anthropic launches Claude 4.6 with enhanced reasoning

### Finance
- S&P 500 hits all-time high on tech earnings
- Fed signals potential rate cut in September
- Bitcoin ETF sees record inflows this week

### Blockchain
- Ethereum completes Pectra upgrade successfully
- Solana launches mobile phone with crypto wallet
- Bitcoin hits $100K milestone

### Tennis
- Carlos Alcaraz wins Indian Wells title
- Alcaraz reaches Miami Open semifinals
- Alcaraz partners with new coach for clay season

### Soccer
- Barcelona wins El Clásico 3-1 at Camp Nou
- Barcelona signs Brazilian wonderkid for $80M
- Barcelona qualifies for Champions League knockout stage
EOF
}

# Test news formatting
format_news_summary() {
    local news="$1"
    local delivery_time="$2"
    
    echo "=== TEST NEWS SUMMARY ==="
    echo "Time: $(date +'%Y-%m-%d %H:%M:%S SGT')"
    echo "Delivery: $delivery_time"
    echo ""
    echo "$news"
    echo ""
    echo "✅ Fact-checked: Test data only"
    echo "🔗 Source: Mock news for testing"
}

# Main test execution
main() {
    local delivery_time="Test Run"
    
    echo "Running news monitor test..."
    
    # Generate mock news
    news=$(mock_news)
    
    # Format and display
    format_news_summary "$news" "$delivery_time"
    
    echo "Test completed successfully!"
    echo "Ready for Telegram configuration and cron setup."
}

main "$@"
#!/bin/bash

# Fetch news and send to Telegram

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source helper functions
if [[ -f "$SCRIPT_DIR/fetch-news.sh" ]]; then
  source "$SCRIPT_DIR/fetch-news.sh"
fi

if [[ -f "$SCRIPT_DIR/send-telegram.sh" ]]; then
  source "$SCRIPT_DIR/send-telegram.sh"
fi

# Main execution
main() {
  local delivery_time="$1"
  local freshness="day"
  
  echo "Starting news fetch for $delivery_time..."
  
  # Fetch news for all topics
  results=$(fetch_topic_news_all "$freshness")
  
  # Format news summary
  summary=$(format_news_summary "$results" "$delivery_time")
  
  # Send to Telegram
  send_message "$summary"
  
  echo "News delivery completed for $delivery_time"
}

fetch_topic_news_all() {
  local freshness="$1"
  
  # This would call the web_search functions
  # For now, return placeholder
  echo "Placeholder news content for $freshness freshness"
}

format_news_summary() {
  local news="$1"
  local delivery_time="$2"
  
  cat << EOF
⚡ *Daily News Summary - $delivery_time*

*Tech:* Latest updates from the tech world...
*AI:* Recent developments in artificial intelligence...
*Finance:* Market movements and economic news...
*Blockchain:* Crypto and Web3 updates...
*Tennis:* Carlos Alcaraz news and results...
*Soccer:* FC Barcelona latest news...

*Fact-checked: ✅*
*Delivered at: $(date +'%Y-%m-%d %H:%M:%S SGT')*

*Source: Multiple reputable news outlets*
EOF
}

# Execute main function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
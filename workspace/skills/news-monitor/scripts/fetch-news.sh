#!/bin/bash

# News Monitor - Fetch latest news

# Topics and sources
TOPICS=("tech" "ai" "finance" "blockchain" "tennis" "soccer")

# Search queries for each topic
QUERIES=(
  "tech news latest site:ft.com OR site:bloomberg.com OR site:barrons.com OR site:techcrunch.com OR site:theverge.com"
  "AI news latest site:ft.com OR site:bloomberg.com OR site:barrons.com OR site:arstechnica.com OR site:venturebeat.com"
  "finance news latest site:ft.com OR site:bloomberg.com OR site:barrons.com OR site:reuters.com OR site:marketwatch.com"
  "blockchain crypto news latest site:ft.com OR site:bloomberg.com OR site:barrons.com OR site:coindesk.com OR site:cointelegraph.com OR site:decrypt.co"
  "Carlos Alcaraz tennis news latest site:espn.com OR site:atptour.com OR site:tennis.com OR site:ft.com OR site:bloomberg.com"
  "FC Barcelona soccer news latest site:espn.com OR site:fcbarcelona.com OR site:diariogol.com OR site:ft.com OR site:bloomberg.com"
)

# Function to fetch news for a topic
fetch_topic_news() {
  local topic="$1"
  local query="$2"
  local freshness="$3"
  
  echo "Fetching $topic news..."
  
  # Use web_search to get latest news
  results=$(web_search "query=$query&count=5&freshness=$freshness&country=SG&language=en")
  
  echo "$results"
}

# Main execution
main() {
  local freshness="day"
  local all_news=()
  
  for i in "${!TOPICS[@]}"; do
    topic="${TOPICS[$i]}"
    query="${QUERIES[$i]}"
    
    news=$(fetch_topic_news "$topic" "$query" "$freshness")
    all_news+=("$news")
  done
  
  # Format and output news
  format_news "${all_news[@]}"
}

format_news() {
  local -n news_array="$1"
  
  echo "=== Daily News Summary ==="
  echo "Time: $(date +'%Y-%m-%d %H:%M:%S SGT')"
  echo ""
  
  for i in "${!TOPICS[@]}"; do
    topic="${TOPICS[$i]}"
    news="${news_array[$i]}"
    
    echo "### $topic"
    echo "$news" | head -5
    echo ""
  done
}

main "$@"
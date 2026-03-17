#!/bin/bash

# Send news summary to Telegram

# Telegram API endpoint and chat ID (configure these)
TELEGRAM_API="https://api.telegram.org/bot8625186050:AAGJ-BfSs3v4intvZCg7bH3fGE2SIV-oHcA/sendMessage"
CHAT_ID="6202550149"

# Function to send message
send_message() {
  local message="$1"
  local parse_mode="HTML"
  
  echo "Sending to Telegram..."
  
  # Escape special characters
  message=$(echo "$message" | sed 's/\"/\\\"/g')
  
  # Send via curl
  response=$(curl -s -X POST "$TELEGRAM_API" \
    -d chat_id="$CHAT_ID" \
    -d text="$message" \
    -d parse_mode="$parse_mode")
  
  echo "Telegram response: $response"
}

# Main execution
main() {
  local message="$1"
  
  send_message "$message"
}

main "$@"
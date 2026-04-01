
#!/bin/bash

# shows the top 5 most active twitter users

set -euo pipefail

trap 'echo ""; echo "interrupted"; exit 130' INT TERM

CSV_FILE="twitter_dataset.csv"
LOG_FILE="feed-analyzer.log"

# check if file exists
if [[ ! -f "$CSV_FILE" ]]; then
  echo "Error: $CSV_FILE not found"
  exit 1
fi

# check if file is not empty
if [[ ! -s "$CSV_FILE" ]]; then
  echo "Error: $CSV_FILE is empty"
  exit 1
fi

echo "Top 5 Most Active Users:"
echo "========================"

# skip header, grab usernames, count them, sort by highest
RESULTS=$(tail -n +2 "$CSV_FILE" | awk -F',' '{print $2}' | sort | uniq -c | sort -nr | head -n 5)

if [[ -z "$RESULTS" ]]; then
  echo "No results"
  exit 0
fi

echo "$RESULTS"

# log the results
{
  echo "$(date '+%Y-%m-%d %H:%M:%S') - ran feed-analyzer"
  echo "$RESULTS"
  echo "---"
} >> "$LOG_FILE"

echo ""
echo "logged to $LOG_FILE"


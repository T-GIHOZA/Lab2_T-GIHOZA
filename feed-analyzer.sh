
#!/bin/bash
#
# LAB 2: Social Media Data Detective - Bash Feed Analyzer
# ========================================================
# Analyzes Twitter dataset to find the Top 5 Most Active Users.
#
# Usage:
#     bash feed-analyzer.sh
#
# Output:
#     - Displays top 5 usernames with post counts to stdout.
#     - Appends results and timestamp to feed-analyzer.log.
#
# Error Handling:
#     - Checks for missing CSV file.
#     - Checks for empty CSV file.
#     - Graceful exit on SIGINT/SIGTERM.

set -euo pipefail

# === SIGNAL HANDLING FOR GRACEFUL SHUTDOWN ===
trap 'echo ""; echo "feed-analyzer.sh interrupted. Shutting down gracefully."; exit 130' INT TERM

CSV_FILE="twitter_dataset.csv"
LOG_FILE="feed-analyzer.log"

# === ERROR CHECKING ===
# Check if CSV file exists
if [[ ! -f "$CSV_FILE" ]]; then
  echo "Error: $CSV_FILE not found in current directory."
  exit 1
fi

# Check if CSV file is not empty
if [[ ! -s "$CSV_FILE" ]]; then
  echo "Error: $CSV_FILE is empty."
  exit 1
fi

echo "Top 5 Most Active Users:"
echo "========================"

# === MAIN ANALYSIS PIPELINE ===
# 1. tail -n +2: Skip the header row
# 2. awk -F',' '{print $2}': Extract Username column (field 2)
# 3. sort: Sort usernames alphabetically
# 4. uniq -c: Count occurrences of each username
# 5. sort -nr: Sort by count (numeric, reverse = highest first)
# 6. head -n 5: Show only top 5 results

RESULTS=$(tail -n +2 "$CSV_FILE" | awk -F',' '{print $2}' | sort | uniq -c | sort -nr | head -n 5)

if [[ -z "$RESULTS" ]]; then
  echo "No username statistics could be generated."
  exit 0
fi

echo "$RESULTS"

# === LOGGING ===
# Append timestamp and results to log file for audit trail
{
  echo "$(date '+%Y-%m-%d %H:%M:%S') - feed-analyzer run"
  echo "$RESULTS"
  echo "---"
} >> "$LOG_FILE"

echo ""
echo "Results logged to $LOG_FILE"


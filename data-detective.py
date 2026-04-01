#!/usr/bin/env python3
"""
LAB 2: The Social Media Data Detective
======================================
Analyzes Twitter dataset to find viral posts, rank by engagement, and search content.
Uses custom algorithms (no .sort(), .sorted(), or max() functions).

Author: Student
Date: April 2026
"""

import argparse
import csv
import os
import signal
import sys


# === SIGNAL HANDLING FOR GRACEFUL SHUTDOWN ===
def graceful_shutdown(signum, frame):
    """Handle SIGINT and SIGTERM signals for clean exit."""
    signal_name = "SIGINT" if signum == signal.SIGINT else "SIGTERM"
    print(f"\n\nReceived {signal_name}. Shutting down gracefully...")
    sys.exit(0)


# Register signal handlers
for sig in (signal.SIGINT, signal.SIGTERM):
    try:
        signal.signal(sig, graceful_shutdown)
    except Exception:
        pass  # Some platforms may not support all signals


def load_raw_data(filename):
    """Loads the CSV file into a list of dictionaries exactly as it is (messy).
    
    Implements retry loop: if file is missing, user can provide alternate path.
    """
    current_filename = filename
    max_retries = 3
    attempt = 0

    while attempt < max_retries:
        # Check if file exists
        if os.path.isfile(current_filename):
            raw_list = []
            try:
                with open(current_filename, mode="r", encoding="utf-8", newline="") as file:
                    reader = csv.DictReader(file)
                    if reader.fieldnames is None:
                        print(f"Error: CSV '{current_filename}' has no header row.")
                        return []
                    for row in reader:
                        raw_list.append(row)
                return raw_list
            except Exception as e:
                print(f"Error reading '{current_filename}': {e}")
                sys.exit(1)
        else:
            # File not found: offer retry
            print(f"Error: File '{current_filename}' not found.")
            attempt += 1
            if attempt < max_retries:
                print(f"Attempt {attempt} of {max_retries}. Please provide a valid path.")
                try:
                    current_filename = input(f"Enter path to CSV file (or press Enter for '{filename}'): ").strip()
                    if not current_filename:
                        current_filename = filename
                except EOFError:
                    # Handle non-interactive mode (no input available)
                    print("No input available. Exiting.")
                    sys.exit(1)
            else:
                print(f"Failed to load file after {max_retries} attempts. Exiting.")
                sys.exit(1)

    return []


def safe_int(value, field_name="value", row_number=None):
    """
    Safely convert a value to integer.
    
    - Returns 0 if value is None or empty string.
    - Returns int(value) if valid.
    - Prints warning and returns 0 if conversion fails.
    
    Args:
        value: The value to convert.
        field_name: Name of the field (for error messages).
        row_number: Row number (for error messages).
    
    Returns:
        int: The converted value or 0 if conversion fails.
    """
    try:
        if value is None or str(value).strip() == "":
            return 0
        return int(str(value).strip())
    except ValueError:
        location = f" in row {row_number}" if row_number is not None else ""
        print(f"WARNING: Invalid integer for {field_name}{location}: '{value}' -> treating as 0")
        return 0


def clean_data(tweets):
    """
    QUEST 1: The Data Auditor (Handle Missing Fields).
    
    Cleans the dataset by:
    1. Removing tweets with missing or empty Text field.
    2. Replacing missing Likes with 0.
    3. Replacing missing Retweets with 0.
    4. Validating all numeric fields via safe_int().
    
    Args:
        tweets: List of tweet dictionaries from CSV.
    
    Returns:
        List of cleaned tweet dictionaries.
        Prints count of rows fixed or removed.
    """
    clean_list = []
    fixed_count = 0
    row_number = 1

    for tweet in tweets:
        row_number += 1
        # Missing Text: remove this tweet entirely
        text = tweet.get("Text", "")
        if text is None or str(text).strip() == "":
            fixed_count += 1
            continue

        # Missing Likes/Retweets: replace with 0
        likes = tweet.get("Likes", "")
        retweets = tweet.get("Retweets", "")
        if likes is None or str(likes).strip() == "":
            tweet["Likes"] = "0"
            fixed_count += 1
        if retweets is None or str(retweets).strip() == "":
            tweet["Retweets"] = "0"
            fixed_count += 1

        # Normalize numeric fields: convert and validate
        tweet["Likes"] = str(safe_int(tweet.get("Likes"), "Likes", row_number))
        tweet["Retweets"] = str(safe_int(tweet.get("Retweets"), "Retweets", row_number))

        clean_list.append(tweet)

    print(f"Auditor: Fixed or removed {fixed_count} bad rows.")
    return clean_list


def find_viral_tweet(tweets):
    """
    QUEST 2: The Viral Post (Find the Maximum).
    
    Finds the single tweet with the highest number of likes.
    
    Implementation: Manually iterates through all tweets and compares likes.
    Does NOT use max() function per assignment requirements.
    
    Args:
        tweets: List of cleaned tweet dictionaries.
    
    Returns:
        The tweet dictionary with the highest likes, or None if no tweets.
    """
    if not tweets:
        print("No tweet data to evaluate for viral post.")
        return None

    viral = tweets[0]
    # Compare each tweet's likes to find the maximum
    for tweet in tweets:
        if safe_int(tweet.get("Likes", "0"), "Likes") > safe_int(viral.get("Likes", "0"), "Likes"):
            viral = tweet

    print("\n--- Viral Post Found ---")
    print(f"Username: {viral.get('Username', 'N/A')}")
    print(f"Likes: {viral.get('Likes', '0')}")
    print(f"Text: {viral.get('Text', '')}")
    return viral


def custom_sort_by_likes(tweets):
    """
    QUEST 3: The Algorithm Builder (Custom Sort).
    
    Implements BUBBLE SORT to rank tweets by likes in descending order.
    
    Algorithm:
    1. Compare adjacent tweets (tweets[j] vs tweets[j+1]).
    2. If left tweet has fewer likes than right tweet, swap them.
    3. Repeat until the list is fully sorted (no swaps in a pass).
    4. Return the sorted list and display top 10.
    
    Time Complexity: O(n²) - quadratic but demonstrates algorithmic thinking.
    
    CRITICAL: Does NOT use .sort(), .sorted(), or max() per assignment.
    
    Args:
        tweets: List of cleaned tweet dictionaries.
    
    Returns:
        List of tweets sorted by likes (descending).
    """
    if not tweets:
        print("No tweet data to sort.")
        return []

    n = len(tweets)
    sorted_list = tweets.copy()  # Copy to avoid modifying original list

    # Bubble Sort: compare adjacent elements and swap if out of order
    for i in range(n):
        for j in range(0, n - i - 1):
            # Compare likes numerically
            left_likes = safe_int(sorted_list[j].get("Likes", "0"), "Likes")
            right_likes = safe_int(sorted_list[j + 1].get("Likes", "0"), "Likes")
            # Swap if left has fewer likes than right (for descending order)
            if left_likes < right_likes:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]

    print("\n--- Top 10 Most Liked Tweets ---")
    top_10 = sorted_list[:10]
    for idx, tweet in enumerate(top_10, 1):
        text_preview = str(tweet.get("Text", "")).strip().replace("\n", " ")[:50]
        print(f"{idx}. {tweet.get('Username', 'N/A')} | {tweet.get('Likes', '0')} Likes | {text_preview}...")

    return sorted_list


def search_tweets(tweets, keyword):
    """
    QUEST 4: The Content Filter (Search & Extract).
    
    Searches tweets for a specific keyword and extracts matching tweets.
    
    Process:
    1. Iterate through all tweets.
    2. Check if keyword (case-insensitive) is in the Tweet Text.
    3. Append matching tweets to a new results list.
    4. Display count and first 5 matches.
    
    Args:
        tweets: List of cleaned tweet dictionaries.
        keyword: The search term (string).
    
    Returns:
        List of tweets containing the keyword.
    """
    if not keyword:
        print("No search keyword provided.")
        return []

    results = []
    # Iterate through tweets and collect matches using .append()
    for tweet in tweets:
        text = str(tweet.get("Text", ""))
        if keyword.lower() in text.lower():  # Case-insensitive search
            results.append(tweet)

    print(f"\nSearch: Found {len(results)} tweets matching '{keyword}'.")
    # Display first 5 matches (slicing, not forbidden functions)
    for tweet in results[:5]:
        snippet = str(tweet.get("Text", "")).replace("\n", " ")[:70]
        print(f" -> {tweet.get('Username', 'N/A')}: {snippet}...")

    return results


def main():
    """
    Main orchestrator for the Data Detective application.
    
    Workflow:
    1. Parse command-line arguments (CSV file path, search keyword).
    2. Load raw data from CSV (with retry logic for missing files).
    3. Clean the data (remove/fix bad rows).
    4. Run all 4 quests in sequence:
       - QUEST 1: Data Auditor
       - QUEST 2: Viral Post
       - QUEST 3: Custom Sort
       - QUEST 4: Content Filter
    5. Handle errors gracefully at each step.
    """
    parser = argparse.ArgumentParser(description="Twitter dataset detective.")
    parser.add_argument("--csv", default="twitter_dataset.csv", help="Path to twitter dataset CSV file")
    parser.add_argument("--search", default="Python", help="Default search keyword")

    args = parser.parse_args()

    # Load raw data (includes retry loop for missing files)
    tweets = load_raw_data(args.csv)
    if not tweets:
        print("No records found in dataset. Exiting.")
        sys.exit(0)

    # Clean the data (Quest 1)
    cleaned = clean_data(tweets)
    if not cleaned:
        print("No valid tweets after cleaning. Exiting.")
        sys.exit(0)

    # Execute all quests
    find_viral_tweet(cleaned)      # Quest 2
    custom_sort_by_likes(cleaned)  # Quest 3
    print("\n--- Keyword Search ---")
    search_tweets(cleaned, args.search)  # Quest 4


if __name__ == "__main__":
    main()

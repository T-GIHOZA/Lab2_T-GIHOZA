import csv
import os
import sys


def load_raw_data(filename):
    # loads the csv and returns the list of tweets
    # if file doesn't exist, keeps asking for the right path (3 times max)
    current_filename = filename
    max_retries = 3
    attempt = 0

    while attempt < max_retries:
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
            print(f"Error: File '{current_filename}' not found.")
            attempt += 1
            if attempt < max_retries:
                print(f"Attempt {attempt} of {max_retries}. Please provide a valid path.")
                try:
                    current_filename = input(f"Enter path to CSV file (or press Enter for '{filename}'): ").strip()
                    if not current_filename:
                        current_filename = filename
                except EOFError:
                    print("No input available. Exiting.")
                    sys.exit(1)
            else:
                print(f"Failed to load file after {max_retries} attempts. Exiting.")
                sys.exit(1)

    return []


def safe_int(value, field_name="value", row_number=None):
    # safely convert to int, returns 0 if empty or bad value
    try:
        if value is None or str(value).strip() == "":
            return 0
        return int(str(value).strip())
    except ValueError:
        location = f" in row {row_number}" if row_number is not None else ""
        print(f"WARNING: Invalid integer for {field_name}{location}: '{value}' -> treating as 0")
        return 0


def clean_data(tweets):
    # QUEST 1: remove tweets with missing text, fill missing likes/retweets with 0
    clean_list = []
    fixed_count = 0

    for tweet in tweets:
        # check if text is missing or empty
        text = tweet.get("Text", "")
        if not text or str(text).strip() == "":
            fixed_count += 1
            continue

        # check username
        username = tweet.get("Username", "")
        if not username or str(username).strip() == "":
            fixed_count += 1
            continue

        # fix missing likes
        if not tweet.get("Likes") or str(tweet.get("Likes", "")).strip() == "":
            tweet["Likes"] = "0"
            fixed_count += 1
        
        # fix missing retweets
        if not tweet.get("Retweets") or str(tweet.get("Retweets", "")).strip() == "":
            tweet["Retweets"] = "0"
            fixed_count += 1

        # convert to proper ints for validation
        tweet["Likes"] = str(safe_int(tweet.get("Likes"), "Likes"))
        tweet["Retweets"] = str(safe_int(tweet.get("Retweets"), "Retweets"))

        clean_list.append(tweet)

    print(f"Auditor: Fixed or removed {fixed_count} bad rows.")
    return clean_list


def find_viral_tweet(tweets):
    # QUEST 2: find the tweet with the most likes (no max() function)
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
    # QUEST 3: bubble sort tweets by likes (descending), no .sort() allowed
    if not tweets:
        print("No tweet data to sort.")
        return []

    n = len(tweets)
    sorted_list = tweets.copy()

    loading_states = [".", "..", "..."]
    
    print("\nSorting tweets by likes" + loading_states[0], end="", flush=True)
    
    for i in range(n):
        # only update loading indicator on outer loop progress
        state_idx = i % 3
        print("\rSorting tweets by likes" + loading_states[state_idx], end="", flush=True)
        
        for j in range(0, n - i - 1):
            left_likes = safe_int(sorted_list[j].get("Likes", "0"), "Likes")
            right_likes = safe_int(sorted_list[j + 1].get("Likes", "0"), "Likes")
            if left_likes < right_likes:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]

    print("\n\n--- Top 10 Most Liked Tweets ---")
    top_10 = sorted_list[:10]
    for idx, tweet in enumerate(top_10, 1):
        text_preview = str(tweet.get("Text", "")).strip().replace("\n", " ")[:50]
        print(f"{idx}. {tweet.get('Username', 'N/A')} | {tweet.get('Likes', '0')} Likes | {text_preview}...")

    return sorted_list


def search_tweets(tweets, keyword):
    # QUEST 4: find all tweets containing the keyword, show first 5 matches
    if not keyword:
        print("No search keyword provided.")
        return []

    results = []
    # find all tweets with the keyword
    for tweet in tweets:
        text = str(tweet.get("Text", ""))
        if keyword.lower() in text.lower():
            results.append(tweet)

    print(f"\nSearch: Found {len(results)} tweets matching '{keyword}'.")
    
    # show first 5
    print(f"Showing first 5 results:")
    for idx, tweet in enumerate(results[:5], 1):
        snippet = str(tweet.get("Text", "")).replace("\n", " ")[:70]
        print(f"{idx}. {tweet.get('Username', 'N/A')}: {snippet}...")
    
    # ask if user wants to save all results
    if len(results) > 5:
        try:
            save = input(f"\nSave all {len(results)} results to a file? (y/n): ").strip().lower()
            if save == 'y':
                filename = f"search_results_{keyword}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Search Results for: {keyword}\n")
                    f.write(f"Total tweets found: {len(results)}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    for idx, tweet in enumerate(results, 1):
                        f.write(f"{idx}. Username: {tweet.get('Username', 'N/A')}\n")
                        f.write(f"   Likes: {tweet.get('Likes', '0')}\n")
                        f.write(f"   Text: {tweet.get('Text', '')}\n")
                        f.write("-" * 80 + "\n")
                
                print(f"Results saved to {filename}")
        except (EOFError, KeyboardInterrupt):
            print("Skipping save.")

    return results


def main():
    # runs all 4 quests in order
    try:
        tweets = load_raw_data("twitter_dataset.csv")
        print(f"Loaded {len(tweets)} raw tweets.\n")
        
        cleaned = clean_data(tweets)
        if not cleaned:
            print("No valid tweets after cleaning.")
            return

        find_viral_tweet(cleaned)
        custom_sort_by_likes(cleaned)
        
        print("\n--- Keyword Search ---")
        keyword = input("What keyword do you want to search for? ").strip()
        
        if keyword:
            search_tweets(cleaned, keyword)
        else:
            print("No keyword provided.")
    
    except KeyboardInterrupt:
        print("\n\nAre you sure you want to quit? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response == 'y':
                print("Exiting...")
                sys.exit(0)
            else:
                print("Continuing...")
                main()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


if __name__ == "__main__":
    main()

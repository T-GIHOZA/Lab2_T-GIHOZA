# Lab 2: The Social Media Data Detective

So this lab is basically about analyzing a Twitter dataset. The goal is to clean up messy data, find the most popular post, rank tweets, and search for keywords.

## What's in here

The project has two parts:

**data-detective.py** - This does all the heavy lifting. It runs through 4 "quests":
1. First, it cleans the data. If tweets are missing text or numbers, it either removes them or fills in 0s.
2. Then it finds the viral post (the one with the most likes) by comparing each tweet.
3. After that, it sorts all tweets by likes using bubble sort.
4. Finally, it searches for a keyword you give it and shows you which tweets contain that word.

**feed-analyzer.sh** - This is just bash piping stuff together. It counts which Twitter users posted the most and shows you the top 5.

## How to run it

The simplest way is just:
```
python data-detective.py
```

This loads the twitter dataset and searches for "Python" by default. If you want to search for something else or use a different CSV file:
```
python data-detective.py --csv twitter_dataset.csv --search "trending"
```

For the bash script:
```
bash feed-analyzer.sh
```

It spits out the top 5 most active users and saves the results to a log file so you can see what happened each time you ran it.

## About the sorting

The hardest part of this lab was probably the sorting. I used bubble sort - you compare pairs of tweets next to each other. If the one on the left has fewer likes than the one on the right, you swap them. You keep doing this until everything is in the right order. It works and it shows you actually understand how sorting works.

## Error handling

I added some stuff so it doesn't just crash if something goes wrong:
- If the CSV file is missing, it asks you to provide the correct path (you get 3 tries)
- If the data has weird numbers (like "abc" instead of a number), it treats it as 0
- If you hit Ctrl+C, the program shuts down cleanly instead of being ugly about it
- If the CSV is empty or doesn't have a header, it tells you what's wrong

## What you need

Just Python 3 and Bash. No extra packages to install. Both scripts use stuff that comes with Python and Bash by default.

## Testing it out

You can try it like this:
```
python data-detective.py --csv twitter_dataset.csv --search "trending"
bash feed-analyzer.sh
cat feed-analyzer.log
```

The log file keeps a record of every time you ran the analyzer, so you can come back and check what you got before.

## Notes

- When you search, it only shows the first 5 results to keep the output from getting too messy
- The top 10 most-liked tweets are also displayed after the sort
- Everything uses basic list operations and loops

# Lab 2: Data Detective

This is a Twitter dataset analyzer. It cleans up messy data, finds the most popular tweet, sort everything by likes, and then allow user to narrow down their research in the dataset using keywords.

## What the scripts do

**data-detective.py** - Runs 4 quests:
1. Cleans the data (removes bad rows, fills in missing numbers)
2. Finds the viral tweet (highest likes)
3. Sorts all tweets by likes
4. Lets you search for a keyword and shows matching tweets

**feed-analyzer.sh** - Shows you which users posted the most

## How to use it

```bash
python data-detective.py
```

This will run through all 4 quests. When it gets to the search part, it'll ask you what keyword you want to search for.

You can also specify the CSV file if you want:
```bash
python data-detective.py --csv your_file.csv
```

For the bash script:
```bash
bash feed-analyzer.sh
```

It shows top 5 users and logs the results each time you run it.

## The sorting thing

Used bubble sort because we can't use `.sort()`. You compare pairs and swap them if they're out of order. Keep doing it until everything's sorted. Simple but it works.

**Note:** With a large dataset, the sorting will take a bit because bubble sort has to buffer through millions of comparisons. You'll see a loading indicator while it's running. Just be patient and let it finish.

## Stuff that won't crash it

- Missing file? It asks you to try again (3 times max)
- Bad numbers in the data? Treats them as 0
- Hit Ctrl+C? It asks if you're sure before exiting
- Empty CSV or no headers? Tells you what's wrong

## What you need

Python 3 and Bash. That's it. No extra packages.

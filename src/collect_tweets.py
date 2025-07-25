# src/collect_tweets.py

import subprocess
import json
import shlex
import sys

def fetch_tweets_cli(query: str, max_tweets: int = 200):
    """
    Uses snscrape’s CLI via the Python module entry-point to fetch tweets.
    Returns a list of tweet JSON objects.
    """
    # Build the command to invoke snscrape as a module
    cmd = (
        f'python -m snscrape._cli '
        f'twitter-search "{query}" '
        f'--jsonl --max-results {max_tweets}'
    )
    try:
        proc = subprocess.run(
            shlex.split(cmd),
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("Error running snscrape:", e, file=sys.stderr)
        print("STDERR:", e.stderr, file=sys.stderr)
        sys.exit(1)

    # Parse each JSONL line into a Python dict
    return [json.loads(line) for line in proc.stdout.splitlines()]

def save_tweets(tweets: list, filepath: str):
    """
    Save the list of tweet dictionaries as a JSON file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Define your query (with date range) and number of tweets
    query = "Tesla OR #Tesla since:2025-07-01 until:2025-07-24"
    tweets = fetch_tweets_cli(query, max_tweets=200)
    save_tweets(tweets, "data/raw_tesla_tweets.json")
    print(f"Saved {len(tweets)} tweets to data/raw_tesla_tweets.json")

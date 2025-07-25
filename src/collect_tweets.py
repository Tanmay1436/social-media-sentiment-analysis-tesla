# src/collect_tweets.py

import subprocess
import json
import shlex

def fetch_tweets_cli(query, max_tweets=200):
    """
    Calls the snscrape CLI to get tweets as JSONL and returns a list of dicts.
    """
    cmd = f"snscrape --jsonl --max-results {max_tweets} twitter-search \"{query}\""
    # Run the command and capture stdout
    proc = subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=True)
    tweets = []
    for line in proc.stdout.splitlines():
        tweets.append(json.loads(line))
    return tweets

def save_tweets(tweets, filepath):
    """
    Save the list of tweet dicts to a JSON file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    query = "Tesla OR #Tesla since:2025-07-01 until:2025-07-24"
    tweets = fetch_tweets_cli(query, max_tweets=200)
    save_tweets(tweets, "data/raw_tesla_tweets.json")
    print(f"Saved {len(tweets)} tweets to data/raw_tesla_tweets.json")

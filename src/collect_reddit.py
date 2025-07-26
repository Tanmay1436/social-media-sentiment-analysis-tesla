# src/collect_reddit.py

import os
import json
from dotenv import load_dotenv
import praw

def load_credentials():
    load_dotenv()  # reads .env in project root
    return {
        'client_id': os.getenv('REDDIT_CLIENT_ID'),
        'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
        'user_agent': os.getenv('REDDIT_USER_AGENT'),
    }

def fetch_reddit_posts(subreddit: str, limit: int = 200):
    """
    Connects to Reddit via PRAW and fetches the newest posts from a subreddit.
    Returns a list of post dictionaries.
    """
    creds = load_credentials()
    reddit = praw.Reddit(
        client_id=creds['client_id'],
        client_secret=creds['client_secret'],
        user_agent=creds['user_agent']
    )

    posts = []
    for post in reddit.subreddit(subreddit).new(limit=limit):
        posts.append({
            'id': post.id,
            'title': post.title,
            'selftext': post.selftext,
            'created_utc': post.created_utc,
            'score': post.score,
            'num_comments': post.num_comments,
            'url': post.url
        })
    return posts

def save_posts(posts: list, filepath: str):
    """
    Saves the fetched posts list into a JSON file (pretty-printed).
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    subreddit_name = 'Tesla'
    posts = fetch_reddit_posts(subreddit_name, limit=200)
    save_posts(posts, 'data/raw_reddit_tesla.json')
    print(f"Saved {len(posts)} Reddit posts to data/raw_reddit_tesla.json")

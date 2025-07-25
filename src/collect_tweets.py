# src/collect_tweets.py

import json
import snscrape.modules.twitter as sntwitter

def fetch_tweets(query, max_tweets=200):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break
        tweets.append({
            'id': tweet.id,
            'date': tweet.date.isoformat(),
            'content': tweet.content,
            'username': tweet.user.username
        })
    return tweets

def save_tweets(tweets, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    query = 'Tesla OR #Tesla since:2025-07-01 until:2025-07-24'
    tweets = fetch_tweets(query, max_tweets=200)
    save_tweets(tweets, 'data/raw_tesla_tweets.json')
    print(f'Saved {len(tweets)} tweets to data/raw_tesla_tweets.json')

# src/collect_tweets.py

import os
import json
from dotenv import load_dotenv
import tweepy

def load_api_keys():
    load_dotenv()
    return {
        'api_key': os.getenv('TWITTER_API_KEY'),
        'api_secret': os.getenv('TWITTER_API_SECRET'),
        'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
        'access_secret': os.getenv('TWITTER_ACCESS_SECRET'),
    }

def create_api_client(keys):
    auth = tweepy.OAuth1UserHandler(
        keys['api_key'], keys['api_secret'],
        keys['access_token'], keys['access_secret']
    )
    return tweepy.API(auth, wait_on_rate_limit=True)

def fetch_tweets(api, query, max_tweets=100):
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en',
                               tweet_mode='extended').items(max_tweets):
        tweets.append({
            'id': tweet.id_str,
            'created_at': str(tweet.created_at),
            'text': tweet.full_text,
            'user': tweet.user.screen_name
        })
    return tweets

def save_tweets(tweets, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    keys = load_api_keys()
    api = create_api_client(keys)
    query = 'Tesla OR #Tesla'
    tweets = fetch_tweets(api, query, max_tweets=200)
    save_tweets(tweets, 'data/raw_tesla_tweets.json')
    print(f'Saved {len(tweets)} tweets to data/raw_tesla_tweets.json')

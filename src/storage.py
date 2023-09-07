import json
from typing import Dict

from tweet import Tweet


def save_credentials(username_: str, password_: str, filename='credentials.json') -> None:
    with open(f'../{filename}', 'w') as f:
        json.dump({"username": username_, "password": password_}, f)


def load_credentials(filename='credentials.json') -> (str, str):
    try:
        with open(f'../{filename}', 'r') as f:
            data = json.load(f)
            return data["username"], data["password"]
    except FileNotFoundError:
        return None, None


def save_tweets_to_file(tweets: Dict[str, Tweet], filename: str = 'tweets.json') -> True:
    with open(f'../{filename}', 'w') as f:
        json.dump({k: v.to_dict() for k, v in tweets.items()}, f)

    return True


def load_tweets_from_file(filename: str = 'tweets.json') -> Dict[str, Tweet]:
    tweets = {}
    try:
        with open(f'../{filename}', 'r') as f:
            data_ = json.load(f)
            tweets = {k: Tweet.from_dict(v) for k, v in data_.items()}
    except FileNotFoundError:
        pass

    return tweets

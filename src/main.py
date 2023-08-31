import json
import time
from typing import Dict

from selenium.common import StaleElementReferenceException

from driver_setup import driver, load_cookies_for_domain, load_local_storage_for_domain, save_cookies_for_domain, \
    save_local_storage_for_domain
from tweet import Tweet
from twitter_actions import login_to_twitter, search_tweets, get_tweet_elements, extract_tweet_data, reply_to_tweet

use_gpt = True


def save_credentials(username_: str, password_: str, filename='credentials.json'):
    with open(filename, 'w') as f:
        json.dump({"username": username_, "password": password_}, f)


def load_credentials(filename='credentials.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data["username"], data["password"]
    except FileNotFoundError:
        return None, None


def save_tweets_to_file(tweets: Dict[str, Tweet], filename: str = 'tweets.json'):
    with open('../' + filename, 'w') as f:
        json.dump({k: v.to_dict() for k, v in tweets.items()}, f)


def load_tweets_from_file(filename: str = 'tweets.json') -> Dict[str, Tweet]:
    tweets = {}
    try:
        with open('../' + filename, 'r') as f:
            data_ = json.load(f)
            tweets = {k: Tweet.from_dict(v) for k, v in data_.items()}
    except FileNotFoundError:
        print(f"{filename} not found. Starting fresh.")
    return tweets


if __name__ == "__main__":
    # Try to load saved credentials
    username, password = load_credentials()

    # If not available, ask the user
    if username is None or password is None:
        username = input('Enter username: ')
        password = input('Enter password: ')
        save_credentials(username, password)

    # Store the tweets
    parsed_tweets: Dict[str, Tweet] = {}
    replied_tweets: Dict[str, Tweet] = load_tweets_from_file('replied_tweets.json')

    try:
        # Login to Twitter
        if not login_to_twitter(username, password):
            raise Exception('Login failed!')

        # # Load cookies and local storages
        # loaded_cookies_for_twitter = load_cookies_for_domain('../cookies_twitter.pkl')
        # loaded_storage_for_twitter = load_local_storage_for_domain('../local_storage_twitter.pkl')
        #
        # loaded_cookies_for_tweet_gpt = load_cookies_for_domain('../cookies_tweet-gpt.pkl', 'https://tweetgpt.app')
        # loaded_storage_for_tweet_gpt = load_local_storage_for_domain('../local_storage_tweet-gpt.pkl')
        #
        # # Print out status of restoring cookies and local storages
        # print(f"Loaded cookies for Twitter: {loaded_cookies_for_twitter}")
        # print(f"Loaded local storage for Twitter: {loaded_storage_for_twitter}")
        # print(f"Loaded cookies for TweetGPT: {loaded_cookies_for_tweet_gpt}")
        # print(f"Loaded local storage for TweetGPT: {loaded_storage_for_tweet_gpt}")
        #
        # # Save restoration status into single variable
        # restored_session = (loaded_cookies_for_twitter
        #                     and loaded_storage_for_twitter
        #                     and loaded_cookies_for_tweet_gpt
        #                     and loaded_storage_for_tweet_gpt)

        restored_session = False

        if use_gpt:
            if not restored_session:
                input("Please authorize the TweetGPT extension manually. Press Enter to continue...")
            else:
                print("TweetGPT authorized session might be restored from cookies!")
                print("Or session has expired already and needs to be reauthorized.")
                input("Press Enter to continue...")

        time.sleep(5)

        search_query = input("Enter a search query: ")

        # Search tweets
        search_tweets(search_query)

        try:
            for tweet_element in get_tweet_elements():
                tweet = Tweet.from_dict(extract_tweet_data(tweet_element))

                if tweet.id not in replied_tweets:
                    # Store the Tweet object
                    parsed_tweets[tweet.id] = tweet_element

                    print(f"--- #{tweet.id} Processing ...")

                    replied = reply_to_tweet(tweet_element, tweet)

                    if replied:
                        replied_tweets[tweet.id] = tweet

                        print(f"--- #{tweet.id} Replied!")
                else:
                    print(f"--- #{tweet_element.id} Skipping...")
        except StaleElementReferenceException as e:
            print("StaleElementReferenceException! Skipping...")

            # Print the stack trace
            time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Potentially other debugging information here.
        pass
    finally:
        # Save the tweets
        save_tweets_to_file(replied_tweets, 'replied_tweets.json')

        # # the cookies and local storages are populated we need to save them for later
        # save_cookies_for_domain('../cookies_twitter.pkl')
        # save_local_storage_for_domain('../local_storage_twitter.pkl')
        #
        # save_cookies_for_domain('../cookies_tweet-gpt.pkl', 'https://tweetgpt.app')
        # save_local_storage_for_domain('../local_storage_tweet-gpt.pkl')

        # driver.close()

    # Wait until all Chrome windows are closed
    while len(driver.window_handles) > 0:
        time.sleep(1)  # Wait for 1 second before checking again

    driver.quit()

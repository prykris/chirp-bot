import time
from typing import Dict

from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys

from driver_setup import driver
from inputs import prompt_search_queries, prompt_integer, prompt_tweet_gpt_mode
from xpath_map import TWEET_GPT_SUPPORTIVE_BUTTON
from storage import load_credentials, save_credentials, load_tweets_from_file, save_tweets_to_file
from tweet import Tweet
from twitter_actions import login_to_twitter, search_tweets, get_tweet_elements, extract_tweet_data, reply_to_tweet

if __name__ == "__main__":
    print('Starting Chirp Bot v0.3.0!')

    # Try to load saved credentials
    username, password = load_credentials()

    # If not available, ask the user
    if username is None or password is None:
        username = input('Enter username: ')
        password = input('Enter password: ')
        save_credentials(username, password)
        print('Credentials saved to credentials.json, delete this file to change or edit the file manually.')
    else:
        print('Credentials loaded from credentials.json. To switch accounts delete the file or edit it manually.')

    limit = prompt_integer('How many tweets do you want to reply to?', 50)
    sleep_timer = prompt_integer('How many minutes  do you want to wait between each batch of tweets?', 30)

    reply_tone = prompt_tweet_gpt_mode(1)

    # Store the tweets
    parsed_tweets: Dict[str, Tweet] = {}
    replied_tweets: Dict[str, Tweet] = load_tweets_from_file('replied_tweets.json')


    def tweet_has_been_replied_to(id_) -> bool:
        return id_ in replied_tweets.keys()


    print(f"Loaded {len(replied_tweets)} replied tweets from previous session")

    search_queries = prompt_search_queries()

    print('Using the following search queries:')
    for query in search_queries:
        print('    * ' + query)

    try:
        print(f'Logging into Twitter as @{username}...')
        # Login to Twitter
        if not login_to_twitter(username, password):
            raise Exception('Login failed! Check your credentials.')

        input("Please authorize the TweetGPT extension manually. Press Enter to continue...")

        while True:

            replied_total = 0
            for index, query in enumerate(search_queries):
                # Get how many tweets to reply to each query, use one tweet per query as default
                tweets_per_query = max(1, limit // len(search_queries))

                # Add missing tweet because of flooring
                if tweets_per_query * len(search_queries) < limit and index == len(search_queries) - 1:
                    tweets_per_query += 1

                replied_query = 0

                print(f"Searching for tweets with the following query: {query}")
                print(f"Query will be replied to {tweets_per_query} tweets per query")
                print(f"Remaining limit: {limit - replied_total}")

                search_tweets(query)
                time.sleep(3)

                for tweet_element in get_tweet_elements():
                    try:
                        tweet = Tweet.from_dict(extract_tweet_data(tweet_element))
                        tweet_preview = tweet.text[:50].replace("\n", " ")

                        # Store the Tweet object
                        parsed_tweets[tweet.id] = tweet_element

                        print(
                            '\n' * 2,
                            '-' * 80,
                            f'[{tweet.time.format("%b %d, %Y at %I:%M")}] @{tweet.user}: {tweet_preview}...',
                        )

                        if not tweet_has_been_replied_to(tweet.id):

                            replied = reply_to_tweet(tweet_element, tweet, reply_tone)
                            # replied = True

                            if replied:
                                replied_tweets[tweet.id] = tweet
                                print(
                                    f"    * Successfully replied to tweet! [{len(replied_tweets)}/{len(parsed_tweets)}]"
                                )

                                replied_query += 1
                                replied_total += 1

                                if replied_query % tweets_per_query == 0:
                                    break

                        else:
                            print(f"    * Tweet {tweet.id} has already been replied to.")
                    except StaleElementReferenceException:
                        print(" - Tweet was unloaded from DOM. Skipping...")
                        continue
                    except NoSuchElementException as e_:
                        print(f" - Tweet {tweet_element.id} scope lacks an element: {e_.msg}")
                        continue
                    except Exception as e_:
                        print(f" - While processing tweet: {e_}")
                        continue
                    finally:
                        try:

                            action = ActionChains(driver)
                            action.send_keys(Keys.ESCAPE).perform()

                        except NoSuchElementException:
                            print('    * Closing previous tweet was not necessary, no close button found.')
                        except Exception as e_:
                            print(f" - While closing tweet: {e_}")
                            search_tweets(query)

            if replied_total % limit == 0:
                print(f"Replied tweets limit of {limit} reached. Saving replied_tweets.json...")
                save_tweets_to_file(replied_tweets, 'replied_tweets.json')
                print(f"Sleeping for {sleep_timer} minutes before continuing...")
                time.sleep(sleep_timer * 60)

    except Exception as e:
        print(f"MAJOR ERROR OCCURRED: {e}")
        print('This should not happen. Report to the developer!')
        pass
    finally:
        try:
            # Save the tweets and ignore keyboard interrupt
            save_tweets_to_file(replied_tweets, 'replied_tweets.json')
        except KeyboardInterrupt:
            print("Ctrl + C was ignored. Saving replied_tweets.json before exiting. Please don't press it again!")
            save_tweets_to_file(replied_tweets, 'replied_tweets.json')
            raise

        driver.close()

    # Wait until all Chrome windows are closed
    while len(driver.window_handles) > 0:
        time.sleep(1)  # Wait for 1 second before checking again

    driver.quit()

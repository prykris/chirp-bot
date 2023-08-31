import time
from urllib.parse import urlencode

from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from driver_setup import driver
from xpath_map import TWEET_REPLY_BUTTON, TWEET_BUTTON, TWEET_REPLY_INPUT
from tweet import Tweet


def login_to_twitter(username, password) -> bool:
    driver.get("https://twitter.com/login")
    time.sleep(2)

    from selenium.webdriver.common.by import By
    from xpath_map import LOGIN_USERNAME_INPUT, LOGIN_NEXT_BUTTON, LOGIN_PASSWORD_INPUT, LOGIN_BUTTON
    from xpath_map import LOGIN_ERROR_ALERT_SPAN

    # Enter the username
    try:
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, LOGIN_USERNAME_INPUT))
        )

        username_input.send_keys(username)
    except TimeoutException:
        print("No username input detected within 10 seconds, quitting...")
        return False

    # Find "next" button and click it
    driver.find_element(By.XPATH, LOGIN_NEXT_BUTTON).click()

    # Enter the password
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, LOGIN_PASSWORD_INPUT))
        )

        password_input.send_keys(password)
    except TimeoutException:
        print("No password input detected within 10 seconds, quitting...")
        return False

    try:
        # Click the login button
        driver.find_element(By.XPATH, LOGIN_BUTTON).click()

        # Waiting up to 10 seconds for the error message to appear
        error_message_span = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, LOGIN_ERROR_ALERT_SPAN))
        )

        print(error_message_span)

        if error_message_span:
            print("Error message detected! Content: ", error_message_span.text)
            return False

    except TimeoutException:
        print("No error message detected within 10 seconds, proceeding...")

    return True


def search_tweets(query):
    params = {
        'q': query + ' lang:en -filter:retweets -filter:replies',
        'src': 'typed_query'
    }

    search_url = f'https://twitter.com/search?{urlencode(params)}'

    driver.get(search_url)


def get_tweet_elements():
    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']"))
            )

            tweet_elements = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
        except TimeoutException:
            print("No tweet elements detected within 10 seconds, quitting...")
            return

        if len(tweet_elements) == 0:
            print("No more tweets found. Exiting.")
            return

        n = len(tweet_elements)
        for i in range(n):
            tweet_element = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")[i]
            yield tweet_element

        driver.execute_script("arguments[0].scrollIntoView();", tweet_elements[-1])

        # Give time for the tweets to load
        time.sleep(5)


def extract_tweet_data(tweet_element) -> dict:
    tweet_link = tweet_element.find_element(By.XPATH, './/a[contains(@href, "/status/")]').get_attribute('href')
    tweet_id = tweet_link.split('/')[-1]

    tweet_user = tweet_element.find_element(By.XPATH, './/span[contains(@class, "css-901oao css-16my406 r-poiln3 '
                                                      'r-bcqeeo r-qvutc0")]').text
    tweet_text = tweet_element.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
    tweet_time = tweet_element.find_element(By.XPATH, './/time').get_attribute('datetime')

    return {
        'id': tweet_id,
        'user': tweet_user,
        'text': tweet_text,
        'time': tweet_time
    }


def reply_to_tweet(tweet_element: WebElement, tweet: Tweet) -> bool:
    from xpath_map import TWEET_GPT_BUTTON

    time.sleep(5)

    # Click on reply button
    try:
        reply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, TWEET_REPLY_BUTTON))
        )

        reply_button.click()
    except TimeoutException:
        print("No reply button detected within 10 seconds, quitting...")
        return False
    except ElementClickInterceptedException:
        print("Reply button was not clickable within 10 seconds, quitting...")
        return False

    time.sleep(2)

    # Click on tweet gpt button
    tweet_element.find_element(By.XPATH, TWEET_GPT_BUTTON).click()

    time.sleep(1)

    # Press on supportive button
    try:
        initial_windows = driver.window_handles

        supportive_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".gptSelectorContainer .gptSelector:first-child"))
        )

        supportive_button.click()

        time.sleep(8)

        if len(driver.window_handles) > len(initial_windows):
            input('TweetGPT extension opened. Press Enter to continue after you have authorized the extension...')

            supportive_button.click()

            time.sleep(8)
    except TimeoutException:
        print("No supportive button detected within 10 seconds, quitting...")
        return False

    # Remove the signature
    tweet_box = tweet_element.find_element(By.XPATH, TWEET_REPLY_INPUT)

    signature_length = 11

    tweet_box.send_keys(Keys.BACKSPACE * signature_length)

    # Submit the tweet
    try:
        tweet_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, TWEET_BUTTON))
        )

        tweet_button.click()
    except TimeoutException:
        print("No tweet button detected within 10 seconds, quitting...")
        return False
    except ElementClickInterceptedException:
        print("Tweet button was not clickable within 10 seconds, quitting...")
        return False

    return True

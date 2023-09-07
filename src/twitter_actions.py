import time
from urllib.parse import urlencode

from selenium.common import TimeoutException, ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from driver_setup import driver
from xpath_map import TWEET_REPLY_BUTTON, TWEET_BUTTON, TWEET_REPLY_INPUT, TWEET_GPT_SUPPORTIVE_BUTTON, \
    TWEET_CLOSE_BUTTON
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
        # This means successfully logged in!
        pass

    return True


def search_tweets(query: str) -> None:
    params = {
        'q': query + ' lang:en -filter:retweets -filter:replies',
        'src': 'typed_query',
        'f': 'live'
    }

    search_url = f'https://twitter.com/search?{urlencode(params)}'

    driver.get(search_url)


def get_tweet_elements():
    print("Getting tweet elements...")
    running = True

    while running:
        try:
            tweet_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "article[data-testid='tweet']:not([data-replied='true'])"))
            )
            current_offset_top = driver.execute_script(
                "return arguments[0].getBoundingClientRect().top;", tweet_element
            )

            if current_offset_top > 0:
                yield tweet_element
            else:
                print(
                    f" - Tweet above last offset top (current_offset_top: {current_offset_top} < 0), skipped..."
                )
                driver.execute_script("arguments[0].setAttribute('data-replied', 'true')", tweet_element)
                continue

            driver.execute_script("arguments[0].scrollIntoView();", tweet_element)
            driver.execute_script("arguments[0].setAttribute('data-replied', 'true')", tweet_element)

            time.sleep(2)
        except TimeoutException:
            print("No tweet elements detected within 10 seconds, waiting... (Press Ctrl+C to quit)")

            # Take last tweet element and scroll to it
            tweet_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "article[data-testid='tweet']"))
            )

            last_tweet_element = tweet_elements[-1]

            if last_tweet_element:
                driver.execute_script("arguments[0].scrollIntoView();", last_tweet_element)
                print(" - Last tweet element detected, scrolling to it...")
            else:
                print(" - No last tweet element detected, scrolling to bottom of the page")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            continue
        except StaleElementReferenceException:
            print("Stale element reference detected, waiting... (Press Ctrl+C to quit)")
            continue
        except KeyboardInterrupt:
            running = False


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


def reply_to_tweet(tweet_element: WebElement, tweet: Tweet, button_xpath: TWEET_GPT_SUPPORTIVE_BUTTON) -> bool:
    from xpath_map import TWEET_GPT_BUTTON

    # Click on reply button
    try:
        reply_button = tweet_element.find_element(By.XPATH, TWEET_REPLY_BUTTON)

        reply_button.click()
    except NoSuchElementException:
        print("  - No reply button detected within 10 seconds, quitting...")
    except ElementClickInterceptedException:
        print("  - Reply button was not clickable within 10 seconds, quitting...")
        return False

    time.sleep(3)

    # Click on tweet gpt button
    tweet_element.find_element(By.XPATH, TWEET_GPT_BUTTON).click()

    time.sleep(3)

    # Press on supportive button
    try:
        initial_windows = driver.window_handles

        supportive_button = driver.find_element(
            By.XPATH, button_xpath
        )

        supportive_button.click()

        time.sleep(5)

        if len(driver.window_handles) > len(initial_windows):
            input('!!! TweetGPT extension opened. Press Enter to continue after you have authorized the extension...')

            supportive_button.click()

            time.sleep(8)
    except NoSuchElementException:
        print("  - No supportive button detected within 10 seconds, quitting...")
        return False

    # Remove the signature
    tweet_box = tweet_element.find_element(By.XPATH, TWEET_REPLY_INPUT)

    signature_length = 11

    tweet_box.send_keys(Keys.BACKSPACE * signature_length)

    if len(tweet_box.text) > 280:
        print(f"  - Generated Tweet too long {len(tweet_box.text)} > 280, skipping...")
        return False

    # Submit the tweet
    try:
        tweet_button = tweet_element.find_element(By.XPATH, TWEET_BUTTON)

        tweet_button.click()
    except NoSuchElementException:
        print("  - No tweet button detected within 10 seconds, quitting...")
        return False
    except ElementClickInterceptedException:
        print("  - Tweet button was not clickable within 10 seconds, quitting...")
        return False
    except ElementNotInteractableException:
        print("  - Tweet button was not interactable within 10 seconds, quitting...")
        return False
    except Exception as e:
        print('  - Could not submit a reply: ', e)
        return False

    return True

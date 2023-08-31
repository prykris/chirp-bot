import os
import pickle
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def initialize_driver():
    chrome_options = Options()
    extension_path = '../extensions/tweetgpt_2_2_2_0.crx'  # Replace with the actual path
    chrome_options.add_extension(extension_path)

    return webdriver.Chrome(options=chrome_options)


def save_cookies_for_domain(filename, domain: Optional[str] = None):
    if domain:
        driver.get(domain)
        time.sleep(5)

    with open(filename, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies_for_domain(filename, domain: Optional[str] = None):
    if os.path.exists(filename):
        if domain:
            driver.get(domain)
            time.sleep(5)

        with open(filename, 'rb') as file:
            cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        return True
    return False


# Function to save localStorage
def save_local_storage_for_domain(filename, domain: Optional[str] = None):
    if domain:
        driver.get(domain)
        time.sleep(5)

    local_storage = driver.execute_script("return window.localStorage;")
    with open(filename, 'wb') as f:
        pickle.dump(local_storage, f)


# Function to load localStorage
def load_local_storage_for_domain(filename, domain: Optional[str] = None):
    if os.path.exists(filename):
        if domain:
            driver.get(domain)
            time.sleep(5)

        with open(filename, 'rb') as f:
            local_storage = pickle.load(f)
        for key, value in local_storage.items():
            driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
        return True
    return False


driver = initialize_driver()

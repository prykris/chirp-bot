LOGIN_USERNAME_INPUT = '//input[@name="text"][@autocomplete="username"]'
LOGIN_PASSWORD_INPUT = '//input[@name="password"][@type="password"][@autocomplete="current-password"]'

LOGIN_NEXT_BUTTON = ('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div['
                     '2]/div/div/div/div[6]')
LOGIN_BUTTON = ('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div['
                '2]/div/div[1]/div/div/div')

LOGIN_ERROR_ALERT_SPAN = '//div[@role="alert"][contains(@class,"css-1dbjc4n")]//span'

TWEET_WRAPPER = '//div[@data-testid="cellInnerDiv"]'
TWEET_CLOSE_BUTTON = '//div[@data-testid="app-bar-close"]'
TWEET_SAVE_DRAFT_BUTTON = '//div[@data-testid="confirmationSheetConfirm"]'
TWEET_DISCARD_DRAFT_BUTTON = '//div[@data-testid="confirmationSheetCancel"]'

TWEET_REPLY_BUTTON = './/div[@data-testid="reply"]'
TWEET_REPLY_INPUT = '//div[@data-testid="tweetTextarea_0"]'
TWEET_BUTTON = '//div[@data-testid="tweetButton"]'

TWEET_GPT_BUTTON = '//div[@id="gptButton"]'

TWEET_GPT_SUPPORTIVE_BUTTON = '//div[@class="gptSelectorContainer"]/div[1][@class="gptSelector"]'
TWEET_GPT_SNARKY_BUTTON = '//div[@class="gptSelectorContainer"]/div[2][@class="gptSelector"]'
TWEET_GPT_OPTIMISTIC_BUTTON = '//div[@class="gptSelectorContainer"]/div[3][@class="gptSelector"]'
TWEET_GPT_CONTROVERSIAL_BUTTON = '//div[@class="gptSelectorContainer"]/div[4][@class="gptSelector"]'
TWEET_GPT_EXCITED_BUTTON = '//div[@class="gptSelectorContainer"]/div[5][@class="gptSelector"]'
TWEET_GPT_SMART_BUTTON = '//div[@class="gptSelectorContainer"]/div[6][@class="gptSelector"]'
TWEET_GPT_HILLBILLY_BUTTON = '//div[@class="gptSelectorContainer"]/div[7][@class="gptSelector"]'
TWEET_GPT_PIRATE_BUTTON = '//div[@class="gptSelectorContainer"]/div[8][@class="gptSelector"]'
TWEET_GPT_HUMOROUS_BUTTON = '//div[@class="gptSelectorContainer"]/div[9][@class="gptSelector"]'
TWEET_GPT_PASSIVE_AGGRESSIVE_BUTTON = '//div[@class="gptSelectorContainer"]/div[10][@class="gptSelector"]'
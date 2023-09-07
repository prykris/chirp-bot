from xpath_map import TWEET_GPT_SUPPORTIVE_BUTTON, TWEET_GPT_OPTIMISTIC_BUTTON, TWEET_GPT_CONTROVERSIAL_BUTTON, \
    TWEET_GPT_EXCITED_BUTTON, TWEET_GPT_SMART_BUTTON, TWEET_GPT_HILLBILLY_BUTTON, TWEET_GPT_PIRATE_BUTTON, \
    TWEET_GPT_HUMOROUS_BUTTON, TWEET_GPT_PASSIVE_AGGRESSIVE_BUTTON, TWEET_GPT_SNARKY_BUTTON


def prompt_integer(prompt, default) -> int:
    while True:
        try:
            value = input(f'{prompt} [default: {default}]: ')
            if value == "":
                return default
            else:
                value = int(value)
                return value
        except ValueError:
            print("Please enter a valid integer or press Enter to use the default value.")


def prompt_search_queries() -> list[str]:
    while True:
        search_query_input = input("Enter search queries (comma-separated, no empty strings): ").strip()
        search_queries = [item.strip() for item in search_query_input.split(',') if item.strip() != ""]

        if search_queries:
            return search_queries
        else:
            print("Please enter at least one non-empty search query.")


def prompt_tweet_gpt_mode(default: int) -> str:
    print(f"Choose a Tweet GPT mode [{default}]:")
    print("1. Supportive")
    print("2. Snarky")
    print("3. Optimistic")
    print("4. Controversial")
    print("5. Excited")
    print("6. Smart")
    print("7. Hillbilly")
    print("8. Pirate")
    print("9. Humorous")
    print("10. Passive-Aggressive")

    choice = input("Enter the number of your choice: ")

    if choice == "":
        choice = str(default)

    if choice == "1":
        return TWEET_GPT_SUPPORTIVE_BUTTON
    elif choice == "2":
        return TWEET_GPT_SNARKY_BUTTON
    elif choice == "3":
        return TWEET_GPT_OPTIMISTIC_BUTTON
    elif choice == "4":
        return TWEET_GPT_CONTROVERSIAL_BUTTON
    elif choice == "5":
        return TWEET_GPT_EXCITED_BUTTON
    elif choice == "6":
        return TWEET_GPT_SMART_BUTTON
    elif choice == "7":
        return TWEET_GPT_HILLBILLY_BUTTON
    elif choice == "8":
        return TWEET_GPT_PIRATE_BUTTON
    elif choice == "9":
        return TWEET_GPT_HUMOROUS_BUTTON
    elif choice == "10":
        return TWEET_GPT_PASSIVE_AGGRESSIVE_BUTTON
    else:
        print("Invalid choice. Please select a valid option.")
        return prompt_tweet_gpt_mode(default)

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

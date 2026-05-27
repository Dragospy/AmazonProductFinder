import undetected_chromedriver
from search import search_products
from compare import compare_products


def get_url(search_string: str) -> str:
    """Transform a free-text user query into an Amazon-compatible search query."""
    return search_string.replace(" ", "+")


def main() -> None:
    try:
        driver = undetected_chromedriver.Chrome(headless=True)
    except Exception as e:
        print(f"Failed to start the browser driver: {e}")
        return

    products = []
    try:
        while True:
            user_input = input("What would you like to do? \n| Search | Compare | Exit |\n").lower()

            if user_input == "exit":
                break

            if user_input == "search":
                search_string = input("What would you like to search for? \n").lower()
                products = search_products(driver, get_url(search_string)) or []

            elif user_input == "compare":
                if not products:
                    print("You haven't searched for any products yet, so nothing to compare.")
                    continue
                compare_products(driver, products)
    finally:
        driver.close()


if __name__ == "__main__":
    main()

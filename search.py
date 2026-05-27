from bs4 import BeautifulSoup
from product import product, list_products
from os import system

ATTRIBUTES = ['rating', 'name', 'price']  # valid attributes the user can sort by


def _price_key(p: product) -> float:
    """Strip the currency symbol from a price string and return it as a float."""
    return float(p.price[1:])


def _rating_key(p: product) -> float:
    return float(p.rating)


def sort_products(products: list, sorting_type: str) -> list:
    """Return a new list of products sorted by the given attribute.

    Name and price sort ascending; rating sorts descending (best first).
    """
    if sorting_type == 'name':
        return sorted(products, key=lambda p: p.name)
    if sorting_type == 'price':
        return sorted(products, key=_price_key)
    if sorting_type == 'rating':
        return sorted(products, key=_rating_key, reverse=True)
    return list(products)


def process_products(results) -> list:
    """Build a list of up to 10 listable product objects from the parsed HTML results."""
    products = []
    for item in results:
        if len(products) >= 10:
            break

        product_var = product(item)
        if getattr(product_var, "listable", None) is None:
            continue

        products.append(product_var)
    return products


def sort_check(products: list) -> list:
    while True:
        sorting_type = input("How would you like to sort it? \n| Rating | Name | Price\n").lower()
        if sorting_type not in ATTRIBUTES:
            print("Not a valid attribute!")
            continue
        return sort_products(products, sorting_type)


def search_products(driver, search_query: str):
    """Search Amazon for the given query and return the first page of listable products."""
    url = f'https://www.amazon.co.uk/s?k={search_query}'

    try:
        driver.get(url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as e:
        print(f"Failed to load Amazon search page: {e}")
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("div", {'data-component-type': 's-search-result'})

    if not results:
        print("Failed to fetch product details, please try again later")
        return []

    products = process_products(results)
    if not products:
        print("No listable products found for this search.")
        return []

    products = sort_check(products)

    system("clear||cls")
    list_products(products)
    return products

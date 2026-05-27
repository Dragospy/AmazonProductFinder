from bs4 import BeautifulSoup
import time
from os import system
from product import list_products


def _prompt_index(prompt: str, valid_range: range, exclude: int = None) -> int:
    """Prompt the user for a product index until they give a valid one."""
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Please enter a number.")
            continue
        idx = int(raw)
        if idx not in valid_range:
            print(f"Please pick a number between {valid_range.start} and {valid_range.stop - 1}.")
            continue
        if exclude is not None and idx == exclude:
            print("Can't compare an item with itself!")
            continue
        return idx


def _fetch_specs(driver, link: str) -> dict:
    """Fetch the technical specifications table for a single product page."""
    try:
        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as e:
        print(f"Failed to load product page: {e}")
        return {}

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find("table", {'id': 'productDetails_techSpec_section_1'})

    if not table:
        return {}

    specs = {}
    for row in table.find_all('tr'):
        header = row.find('th')
        data = row.find('td')
        if header is None or data is None:
            continue
        specs[header.text.strip()] = data.text.strip()
    return specs


def compare_products(driver, products) -> None:
    system("clear||cls")
    list_products(products)

    valid = range(1, len(products) + 1)
    idx_1 = _prompt_index(
        "Choose a product (number before the name of the product)\n",
        valid,
    )
    idx_2 = _prompt_index(
        "Choose a product to compare it with (number before the name of the product)\n",
        valid,
        exclude=idx_1,
    )

    # the list is 0-indexed, the user input is 1-indexed
    product_1, product_2 = products[idx_1 - 1], products[idx_2 - 1]

    print("\nFetching products (delayed to avoid Amazon bot detection)")
    time.sleep(2)
    specs_1 = _fetch_specs(driver, product_1.link)
    time.sleep(2)
    specs_2 = _fetch_specs(driver, product_2.link)

    if not specs_1 or not specs_2:
        print("Failed to fetch product details for at least one product. Please try again later.")
        return

    system("clear||cls")
    print(f"Product {idx_1} link: {product_1.link}")
    print(f"Product {idx_2} link: {product_2.link}\n")

    for key, value in specs_1.items():
        other = specs_2.get(key, "No Comparable Data Listed")
        print(f"{key}:\n  {idx_1} -> {value}\n  {idx_2} -> {other}\n")

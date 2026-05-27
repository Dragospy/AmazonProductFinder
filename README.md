# Amazon Product Finder

A Python CLI tool that searches Amazon UK for products, sorts them by name, price, or rating, and lets you compare the technical specifications of two products side by side. Uses Selenium with `undetected-chromedriver` to handle Amazon's bot detection, and BeautifulSoup to parse the results.

- Creator: Dragos Soalca (Dragospy / W4TCH3R)

## Why I made this

My name is Dragos.py and I had no Python projects on my GitHub. So I picked something that actually annoys me — browsing Amazon and comparing products — and built a tool for it.

## Requirements

- Python 3.12.8 or newer
- Google Chrome installed (used by `undetected-chromedriver`)

## Installation

```bash
git clone https://github.com/<your-username>/AmazonProductFinder.git
cd AmazonProductFinder
python -m venv .venv
source .venv/bin/activate    # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

You'll get a prompt with three options:

- **Search** — enter a query, then choose how to sort the first page of results (by rating, name, or price). Up to 10 results are returned.
- **Compare** — pick two products from your last search; the tool fetches each product page and prints the technical specifications side by side.
- **Exit** — closes the headless browser and quits.

## Project structure

```
AmazonProductFinder/
├── main.py            # Entry point and main interactive loop
├── search.py          # Search query handling, parsing, and sorting
├── compare.py         # Side-by-side spec comparison logic
├── product.py         # Product data model and parsing from HTML
├── config.py          # Configuration (Amazon TLD, etc.)
├── requirements.txt   # Runtime dependencies
├── requirements-dev.txt
└── tests/
    └── test_sort.py   # Unit tests for sorting logic
```

## Running the tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

## Notes

- The tool currently scrapes `amazon.co.uk`. To target a different Amazon region, edit `link_end` in `config.py`.
- Amazon actively changes its HTML and runs bot-detection. If parsing breaks, the selectors in `product.py` and `compare.py` are the first place to look.

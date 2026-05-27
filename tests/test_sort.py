"""Unit tests for product sorting logic."""
import os
import sys
from dataclasses import dataclass

# allow `import search` from the project root when pytest is run from anywhere
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from search import sort_products


@dataclass
class FakeProduct:
    """A lightweight stand-in for the real product class for testing sort logic."""
    name: str
    price: str
    rating: str


def _sample_products():
    return [
        FakeProduct(name="Charlie Headphones", price="£49.99", rating="4.5"),
        FakeProduct(name="Alpha Speaker",      price="£19.99", rating="3.8"),
        FakeProduct(name="Bravo Earbuds",      price="£99.00", rating="4.9"),
    ]


def test_sort_by_name_ascending():
    sorted_products = sort_products(_sample_products(), "name")
    assert [p.name for p in sorted_products] == [
        "Alpha Speaker",
        "Bravo Earbuds",
        "Charlie Headphones",
    ]


def test_sort_by_price_ascending():
    sorted_products = sort_products(_sample_products(), "price")
    assert [p.price for p in sorted_products] == ["£19.99", "£49.99", "£99.00"]


def test_sort_by_rating_descending():
    sorted_products = sort_products(_sample_products(), "rating")
    assert [p.rating for p in sorted_products] == ["4.9", "4.5", "3.8"]


def test_sort_does_not_mutate_original():
    original = _sample_products()
    original_order = [p.name for p in original]
    sort_products(original, "price")
    assert [p.name for p in original] == original_order


def test_unknown_sort_type_returns_unchanged_copy():
    original = _sample_products()
    result = sort_products(original, "weight")
    assert [p.name for p in result] == [p.name for p in original]
    assert result is not original  # should still be a fresh list


def test_sort_empty_list():
    assert sort_products([], "price") == []

from playwright.sync_api import Page,expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps


def test_count_catalog(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")
    assert steps.get_products_count() == 6

def test_sorted_by_name(page):
    steps = CatalogPage(page)
    steps.login("standard_user", "secret_sauce")

    steps.sort_items("az")
    assert steps.get_product_names() == sorted(steps.get_product_names())

    steps.sort_items("za")
    assert steps.get_product_names() == sorted(steps.get_product_names(), reverse=True)

def test_sort_by_price(page):
    steps = CatalogPage(page)
    steps.login("standard_user", "secret_sauce")

    steps.sort_items("lohi")
    assert steps.get_product_prices() == sorted(steps.get_product_prices())

    steps.sort_items("hilo")
    assert steps.get_product_prices() == sorted(steps.get_product_prices(), reverse=True)

def test_add_to_card(page):
    steps = CatalogPage(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Bike Light")
    assert steps.get_cart_count() == 1

def test_add_and_remove_onesie(page):
    steps = CatalogPage(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 1

    steps.remove_from_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 0


def test_product_details_onesie(page):
    steps = CatalogPage(page)
    steps.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Onesie")

    assert name == detail_name
    assert price == detail_price

def test_product_details_fleece_jacket(page):
    steps = CatalogPage(page)
    steps.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = steps.open_product_details("Fleece Jacket")

    assert name == detail_name
    assert price == detail_price


def test_remove_item_from_catalog(page):
    steps = CatalogPage(page)
    steps.login("standard_user", "secret_sauce")

    remove_button = steps.remove_from_cart("Test.allTheThings() T-Shirt (Red)")
    expect(remove_button).to_have_text("Add to cart")



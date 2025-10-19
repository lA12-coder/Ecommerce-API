import pytest


def test_category_slug_autogenerates(category):
    assert category.slug


def test_product_slug_autogenerates(product):
    assert product.slug


def test_variant_price_fallback_to_product_price(product, variant):
    assert variant.get_price() == variant.price
    variant.price = None
    assert variant.get_price() == product.price



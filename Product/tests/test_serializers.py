import pytest
from Product.serializer import ProductListSerializer, CategorySerializer, VariantSerializer


def test_category_serializer_fields(category):
    serializer = CategorySerializer(instance=category)
    assert set(serializer.data.keys()) >= {"id", "name", "slug", "parent", "description"}


def test_product_list_serializer_relations(product, variant):
    serializer = ProductListSerializer(instance=product)
    data = serializer.data
    assert "images" in data
    assert "variants" in data
    assert isinstance(data["category"], list)


def test_variant_serializer_fields(variant):
    serializer = VariantSerializer(instance=variant)
    assert set(serializer.data.keys()) >= {"id", "product", "name", "sku", "price", "stock", "is_active"}



import pytest
from django.contrib.auth import get_user_model
from Product.models import Category, Product, Variant


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(email="test@example.com", password="password123")


@pytest.fixture
def category(db):
    return Category.objects.create(name="Shoes")


@pytest.fixture
def product(db, category):
    product = Product.objects.create(
        title="Running Shoe",
        description="Lightweight running shoe",
        price="99.99",
        currency="USD",
        sku="SKU-001",
        stock=10,
    )
    product.category.add(category)
    return product


@pytest.fixture
def variant(db, product):
    return Variant.objects.create(product=product, name="Size 42 / Blue", sku="SKU-001-42B", price="109.99", stock=5)



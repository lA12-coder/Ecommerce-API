import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


def test_list_products(api_client, product):
    response = api_client.get('/api/products/')
    assert response.status_code == 200
    assert response.data['count'] >= 1


def test_search_products_by_title(api_client, product):
    response = api_client.get('/api/products/?search=Running')
    assert response.status_code == 200
    titles = [item['title'] for item in response.data['results']]
    assert any('Running' in t for t in titles)



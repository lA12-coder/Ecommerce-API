from django_filters import FilterSet, NumberFilter, CharFilter
from rest_framework import filters
from .models import Product

class ProductFilter(FilterSet):
    price_min = NumberFilter(field_name='price', lookup_expr="gte")
    price_max = NumberFilter(field_name="price", lookup_expr="lte")
    category = CharFilter(field_name="category", lookup_expr="iexact")

    class Meta:
        model = Product
        fields = ["price_min", "price_max", "category", "is_active"]


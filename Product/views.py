from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from Product.models import Product, Category, ProductImage, Variant
from User.permissions import IsAdminOrReadOnly
from .serializer import ProductListSerializer, CategorySerializer, ProductImageSerializer, VariantSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("images", "variants").all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ("title","category", "sku", "description")
    ordering_fields = ("price", "created_at","title")
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Product.objects.all()
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes =  [IsAdminOrReadOnly]

class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes =  [IsAdminOrReadOnly]


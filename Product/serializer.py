from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from Product.models import Product, Category, ProductImage, Variant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("id",)

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    class Meta:
        model = ProductImage
        fields = ("id", "product", "image", "alt_text", "order")
        read_only_fields = ("id",)

    def validate_image(self, image):
        max_size = 5 * 1024 * 1024
        if image.size > max_size:
            raise ValidationError("Image file too large (max 5 MB).")
        valid_mime_type = ["image/jpeg", "image/png", "image/webp"]
        content_type = image.content_type
        if content_type not in valid_mime_type:
            raise ValidationError("Unsupported image type. Use JPEG/PNG/WEBP")
        return image
class ProductImageBase64Serializer(serializers.ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model = ProductImage
        fields = ("id", "product", "image", "alt_text", "order")


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"
        read_only_fields = ("id",)


class ProductListSerializer(serializers.ModelSerializer):
    category  = CategorySerializer(read_only=True)
    images = ProductImageSerializer(read_only=True, many=True)
    variant = VariantSerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ("id","title", "sku", "description", "slug","price", "currency", "is_active", "category", "images","variant", "created_at", "updated_at")
        read_only_fields = ("id", "sku", "slug", "created_at", "updates_at")


from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'sku', 'category__name', 'is_active')
    search_fields = ('title', 'description', 'sku')
    list_filter = ('is_active', 'category')

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'sku', 'price', 'stock', 'is_active')
    search_fields = ('product__title', 'name', 'sku')
    list_filter = ('is_active',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'order')

from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['id', 'unit_price', 'total_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        'cart', 'product', 'variant', 'quantity', 
        'unit_price', 'total_price'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['cart__user__email', 'product__title']
    readonly_fields = ['id', 'unit_price', 'total_price']

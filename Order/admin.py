from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['id', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'status', 'total_amount', 
        'payment_status', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__email']
    readonly_fields = ['id', 'order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'order_number', 'user', 'status')
        }),
        ('Financial', {
            'fields': ('subtotal', 'tax_amount', 'shipping_cost', 'total_amount')
        }),
        ('Addresses', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('Payment', {
            'fields': ('payment_status', 'payment_method')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at')
        })
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'product', 'variant', 'quantity', 
        'unit_price', 'total_price'
    ]
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'product__title']
    readonly_fields = ['id', 'unit_price', 'total_price']

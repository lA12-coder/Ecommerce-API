from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from Cart.models import Cart, CartItem
from User.models import Address
from Product.models import Product, Variant


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem"""
    product_title = serializers.CharField(source='product.title', read_only=True)
    variant_name = serializers.CharField(source='variant.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'variant', 'product_title', 'variant_name',
            'quantity', 'unit_price', 'total_price'
        ]
        read_only_fields = ['id', 'unit_price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    shipping_address_line1 = serializers.CharField(source='shipping_address.line1', read_only=True)
    shipping_address_city = serializers.CharField(source='shipping_address.city', read_only=True)
    billing_address_line1 = serializers.CharField(source='billing_address.line1', read_only=True)
    billing_address_city = serializers.CharField(source='billing_address.city', read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_email', 'status',
            'subtotal', 'tax_amount', 'shipping_cost', 'total_amount',
            'shipping_address', 'billing_address', 'shipping_address_line1',
            'shipping_address_city', 'billing_address_line1', 'billing_address_city',
            'payment_status', 'payment_method', 'created_at', 'updated_at',
            'confirmed_at', 'shipped_at', 'delivered_at', 'items', 'total_items'
        ]
        read_only_fields = [
            'id', 'order_number', 'user', 'subtotal', 'tax_amount',
            'shipping_cost', 'total_amount', 'created_at', 'updated_at',
            'confirmed_at', 'shipped_at', 'delivered_at'
        ]


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating orders from cart"""
    shipping_address_id = serializers.UUIDField()
    billing_address_id = serializers.UUIDField()
    payment_method = serializers.CharField(max_length=50, required=False, default='')
    
    def validate_shipping_address_id(self, value):
        """Validate shipping address belongs to user"""
        try:
            address = Address.objects.get(id=value, user=self.context['request'].user)
            return value
        except Address.DoesNotExist:
            raise serializers.ValidationError("Shipping address not found or doesn't belong to you")
    
    def validate_billing_address_id(self, value):
        """Validate billing address belongs to user"""
        try:
            address = Address.objects.get(id=value, user=self.context['request'].user)
            return value
        except Address.DoesNotExist:
            raise serializers.ValidationError("Billing address not found or doesn't belong to you")
    
    def validate(self, attrs):
        """Validate cart has items and stock availability"""
        user = self.context['request'].user
        
        # Check if user has a cart with items
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("No cart found for user")
        
        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty")
        
        # Check stock availability for all cart items
        for cart_item in cart.items.all():
            available_stock = cart_item.variant.stock if cart_item.variant else cart_item.product.stock
            if cart_item.quantity > available_stock:
                raise serializers.ValidationError(
                    f"Insufficient stock for {cart_item.product.title}. "
                    f"Available: {available_stock}, Requested: {cart_item.quantity}"
                )
        
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        """Create order from cart"""
        user = self.context['request'].user
        
        # Get user's cart
        cart = Cart.objects.get(user=user)
        
        # Get addresses
        shipping_address = Address.objects.get(id=validated_data['shipping_address_id'])
        billing_address = Address.objects.get(id=validated_data['billing_address_id'])
        
        # Create order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            billing_address=billing_address,
            payment_method=validated_data.get('payment_method', ''),
            subtotal=0,  # Will be calculated
            total_amount=0  # Will be calculated
        )
        
        # Create order items from cart items
        for cart_item in cart.items.all():
            unit_price = cart_item.unit_price
            
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                quantity=cart_item.quantity,
                unit_price=unit_price
            )
        
        # Calculate totals
        order.calculate_totals()
        order.save()
        
        # Clear the cart
        cart.clear()
        
        return order


class UpdateOrderStatusSerializer(serializers.Serializer):
    """Serializer for updating order status (admin only)"""
    status = serializers.ChoiceField(choices=Order.Status.choices)
    
    def validate_status(self, value):
        """Validate status transition"""
        order = self.context['order']
        current_status = order.status
        
        # Define valid status transitions
        valid_transitions = {
            Order.Status.PENDING: [Order.Status.CONFIRMED, Order.Status.CANCELLED],
            Order.Status.CONFIRMED: [Order.Status.PROCESSING, Order.Status.CANCELLED],
            Order.Status.PROCESSING: [Order.Status.SHIPPED, Order.Status.CANCELLED],
            Order.Status.SHIPPED: [Order.Status.DELIVERED],
            Order.Status.DELIVERED: [Order.Status.REFUNDED],
            Order.Status.CANCELLED: [],
            Order.Status.REFUNDED: []
        }
        
        if value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot change status from {current_status} to {value}"
            )
        
        return value

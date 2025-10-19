from rest_framework import serializers
from django.db import transaction
from .models import Cart, CartItem
from Product.models import Product, Variant


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem"""
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    variant_name = serializers.CharField(source='variant.name', read_only=True)
    variant_price = serializers.DecimalField(source='variant.get_price', max_digits=10, decimal_places=2, read_only=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'variant', 'product_title', 'product_price',
            'variant_name', 'variant_price', 'quantity', 'unit_price', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart"""
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items', 'total_items', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart"""
    product_id = serializers.UUIDField()
    variant_id = serializers.UUIDField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, default=1)
    
    def validate_product_id(self, value):
        """Validate product exists and is active"""
        try:
            product = Product.objects.get(id=value, is_active=True)
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or inactive")
    
    def validate_variant_id(self, value):
        """Validate variant exists and is active"""
        if value:
            try:
                variant = Variant.objects.get(id=value, is_active=True)
                return value
            except Variant.DoesNotExist:
                raise serializers.ValidationError("Variant not found or inactive")
        return value
    
    def validate(self, attrs):
        """Validate variant belongs to product and stock availability"""
        product_id = attrs['product_id']
        variant_id = attrs.get('variant_id')
        quantity = attrs['quantity']
        
        product = Product.objects.get(id=product_id)
        
        if variant_id:
            variant = Variant.objects.get(id=variant_id)
            if variant.product != product:
                raise serializers.ValidationError("Variant does not belong to the selected product")
            
            if variant.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock. Available: {variant.stock}, Requested: {quantity}"
                )
        else:
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock. Available: {product.stock}, Requested: {quantity}"
                )
        
        return attrs
    
    def create(self, validated_data):
        """Add item to cart"""
        cart = validated_data['cart']
        product = Product.objects.get(id=validated_data['product_id'])
        variant = Variant.objects.get(id=validated_data['variant_id']) if validated_data.get('variant_id') else None
        quantity = validated_data['quantity']
        
        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()
        
        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    """Serializer for updating cart item quantity"""
    quantity = serializers.IntegerField(min_value=1)
    
    class Meta:
        model = CartItem
        fields = ['quantity']
    
    def validate_quantity(self, value):
        """Validate quantity against available stock"""
        cart_item = self.instance
        available_stock = cart_item.variant.stock if cart_item.variant else cart_item.product.stock
        
        if value > available_stock:
            raise serializers.ValidationError(
                f"Insufficient stock. Available: {available_stock}, Requested: {value}"
            )
        
        return value

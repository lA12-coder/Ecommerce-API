from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer, UpdateCartItemSerializer
from Product.models import Product, Variant


class CartView(generics.RetrieveAPIView):
    """Get user's cart"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Get or create cart for user"""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartItemListCreateView(generics.ListCreateAPIView):
    """List cart items and add items to cart"""
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return cart items for the authenticated user"""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)
    
    def get_serializer_class(self):
        """Use different serializer for creation"""
        if self.request.method == 'POST':
            return AddToCartSerializer
        return CartItemSerializer
    
    def perform_create(self, serializer):
        """Add item to cart"""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a cart item"""
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return cart items for the authenticated user"""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)
    
    def get_serializer_class(self):
        """Use different serializer for updates"""
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateCartItemSerializer
        return CartItemSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    """Add product to cart"""
    serializer = AddToCartSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        try:
            cart_item = serializer.save()
            response_serializer = CartItemSerializer(cart_item)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def clear_cart(request):
    """Clear all items from cart"""
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.clear()
        return Response({'message': 'Cart cleared successfully'})
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def cart_summary(request):
    """Get cart summary (total items, total price)"""
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        summary = {
            'total_items': cart.total_items,
            'total_price': str(cart.total_price),
            'items_count': cart.items.count()
        }
        
        return Response(summary)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from .models import Order, OrderItem
from .serializers import (
    OrderSerializer, CreateOrderSerializer, UpdateOrderStatusSerializer
)
from User.models import User


class OrderListCreateView(generics.ListCreateAPIView):
    """List user's orders and create new orders from cart"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return orders for the authenticated user"""
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializer for creation"""
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """Create order from cart"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            order = serializer.save()
            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderDetailView(generics.RetrieveAPIView):
    """Retrieve a specific order"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return orders for the authenticated user"""
        return Order.objects.filter(user=self.request.user)


class UserOrderListView(generics.ListAPIView):
    """List orders for a specific user (admin only)"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_queryset(self):
        """Return orders for the specified user"""
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return Order.objects.filter(user=user)


class OrderStatusUpdateView(generics.UpdateAPIView):
    """Update order status (admin only)"""
    serializer_class = UpdateOrderStatusSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_queryset(self):
        """Return all orders for admin"""
        return Order.objects.all()
    
    def update(self, request, *args, **kwargs):
        """Update order status with validation"""
        order = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'order': order})
        serializer.is_valid(raise_exception=True)
        
        new_status = serializer.validated_data['status']
        old_status = order.status
        
        try:
            with transaction.atomic():
                # Handle specific status transitions
                if new_status == Order.Status.CONFIRMED and old_status == Order.Status.PENDING:
                    order.confirm()
                elif new_status == Order.Status.CANCELLED and order.can_be_cancelled():
                    order.cancel()
                elif new_status == Order.Status.SHIPPED and old_status == Order.Status.PROCESSING:
                    order.status = new_status
                    order.shipped_at = timezone.now()
                    order.save()
                elif new_status == Order.Status.DELIVERED and old_status == Order.Status.SHIPPED:
                    order.status = new_status
                    order.delivered_at = timezone.now()
                    order.save()
                else:
                    order.status = new_status
                    order.save()
                
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data)
                
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_order(request, order_id):
    """Cancel an order (user can only cancel their own orders)"""
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        if not order.can_be_cancelled():
            return Response(
                {'error': 'Order cannot be cancelled in its current status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            order.cancel()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def order_statistics(request):
    """Get order statistics for the authenticated user"""
    user = request.user
    
    orders = Order.objects.filter(user=user)
    
    stats = {
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status=Order.Status.PENDING).count(),
        'confirmed_orders': orders.filter(status=Order.Status.CONFIRMED).count(),
        'shipped_orders': orders.filter(status=Order.Status.SHIPPED).count(),
        'delivered_orders': orders.filter(status=Order.Status.DELIVERED).count(),
        'cancelled_orders': orders.filter(status=Order.Status.CANCELLED).count(),
        'total_spent': sum(order.total_amount for order in orders.filter(
            status__in=[Order.Status.CONFIRMED, Order.Status.PROCESSING, 
                       Order.Status.SHIPPED, Order.Status.DELIVERED]
        ))
    }
    
    return Response(stats)

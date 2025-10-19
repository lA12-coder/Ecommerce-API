from django.urls import path
from . import views

urlpatterns = [
    # Order endpoints
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<uuid:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<uuid:order_id>/cancel/', views.cancel_order, name='order-cancel'),
    path('orders/statistics/', views.order_statistics, name='order-statistics'),
    
    # Admin endpoints
    path('users/<uuid:user_id>/orders/', views.UserOrderListView.as_view(), name='user-orders'),
    path('orders/<uuid:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
]

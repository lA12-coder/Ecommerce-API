from django.urls import path
from . import views

urlpatterns = [
    # Cart endpoints
    path('cart/', views.CartView.as_view(), name='cart-detail'),
    path('cart/items/', views.CartItemListCreateView.as_view(), name='cart-item-list-create'),
    path('cart/items/<uuid:pk>/', views.CartItemDetailView.as_view(), name='cart-item-detail'),
    path('cart/add/', views.add_to_cart, name='add-to-cart'),
    path('cart/clear/', views.clear_cart, name='clear-cart'),
    path('cart/summary/', views.cart_summary, name='cart-summary'),
]

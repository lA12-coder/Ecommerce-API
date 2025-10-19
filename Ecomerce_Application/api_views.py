from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API Root - Lists all available endpoints
    """
    base_url = request.build_absolute_uri('/')
    
    endpoints = {
        "message": "E-commerce API",
        "version": "1.0.0",
        "documentation": f"{base_url}api/docs/",
        "schema": f"{base_url}api/schema/",
        "endpoints": {
            "authentication": {
                "login": f"{base_url}api/auth/jwt/create/",
                "refresh": f"{base_url}api/auth/jwt/refresh/",
                "logout": f"{base_url}api/auth/jwt/logout/",
                "register": f"{base_url}api/auth/users/",
                "user_profile": f"{base_url}api/auth/users/me/",
                "password_reset": f"{base_url}api/auth/users/reset_password/",
                "password_reset_confirm": f"{base_url}api/auth/users/reset_password_confirm/",
            },
            "users": {
                "list_users": f"{base_url}api/users/",
                "user_detail": f"{base_url}api/users/{{user_id}}/",
                "user_addresses": f"{base_url}api/users/{{user_id}}/addresses/",
                "user_orders": f"{base_url}api/users/{{user_id}}/orders/",
            },
            "products": {
                "list_products": f"{base_url}api/products/",
                "product_detail": f"{base_url}api/products/{{product_id}}/",
                "product_variants": f"{base_url}api/products/{{product_id}}/variants/",
                "product_images": f"{base_url}api/products/{{product_id}}/images/",
                "search_products": f"{base_url}api/products/?search={{query}}",
                "filter_by_category": f"{base_url}api/products/?category={{category_id}}",
            },
            "categories": {
                "list_categories": f"{base_url}api/categories/",
                "category_detail": f"{base_url}api/categories/{{category_id}}/",
                "category_products": f"{base_url}api/categories/{{category_id}}/products/",
            },
            "variants": {
                "list_variants": f"{base_url}api/variants/",
                "variant_detail": f"{base_url}api/variants/{{variant_id}}/",
            },
            "cart": {
                "get_cart": f"{base_url}api/cart/",
                "cart_items": f"{base_url}api/cart/items/",
                "add_to_cart": f"{base_url}api/cart/add/",
                "update_cart_item": f"{base_url}api/cart/items/{{item_id}}/",
                "remove_cart_item": f"{base_url}api/cart/items/{{item_id}}/",
                "clear_cart": f"{base_url}api/cart/clear/",
                "cart_summary": f"{base_url}api/cart/summary/",
            },
            "orders": {
                "list_orders": f"{base_url}api/orders/",
                "create_order": f"{base_url}api/orders/",
                "order_detail": f"{base_url}api/orders/{{order_id}}/",
                "cancel_order": f"{base_url}api/orders/{{order_id}}/cancel/",
                "order_statistics": f"{base_url}api/orders/statistics/",
                "user_orders": f"{base_url}api/users/{{user_id}}/orders/",
                "update_order_status": f"{base_url}api/orders/{{order_id}}/status/",
            },
            "admin": {
                "admin_panel": f"{base_url}admin/",
                "api_docs": f"{base_url}api/docs/",
            }
        },
        "authentication": {
            "required": "Most endpoints require JWT authentication",
            "header_format": "Authorization: Bearer <your_jwt_token>",
            "get_token": f"{base_url}api/auth/jwt/create/",
        },
        "pagination": {
            "default_page_size": 12,
            "page_parameter": "?page={{page_number}}",
            "page_size_parameter": "?page_size={{size}}",
        },
        "filtering": {
            "search": "?search={{query}}",
            "ordering": "?ordering={{field}}",
            "filtering": "?{{field}}={{value}}",
        },
        "examples": {
            "get_products": f"{base_url}api/products/?search=running&page=1",
            "add_to_cart": {
                "method": "POST",
                "url": f"{base_url}api/cart/add/",
                "body": {
                    "product_id": "uuid",
                    "variant_id": "uuid (optional)",
                    "quantity": 1
                }
            },
            "create_order": {
                "method": "POST",
                "url": f"{base_url}api/orders/",
                "body": {
                    "shipping_address_id": "uuid",
                    "billing_address_id": "uuid",
                    "payment_method": "credit_card"
                }
            }
        }
    }
    
    return Response(endpoints)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_documentation(request):
    """
    Detailed API Documentation with examples and usage instructions
    """
    base_url = request.build_absolute_uri('/')
    
    documentation = {
        "title": "E-commerce API Documentation",
        "version": "1.0.0",
        "description": "A comprehensive e-commerce API built with Django REST Framework",
        "base_url": base_url,
        
        "getting_started": {
            "authentication": {
                "description": "This API uses JWT (JSON Web Token) authentication",
                "steps": [
                    "1. Register a new user: POST /api/auth/users/",
                    "2. Login to get JWT token: POST /api/auth/jwt/create/",
                    "3. Include token in headers: Authorization: Bearer <your_token>",
                    "4. Use the token for authenticated requests"
                ],
                "example_login": {
                    "url": f"{base_url}api/auth/jwt/create/",
                    "method": "POST",
                    "body": {
                        "email": "user@example.com",
                        "password": "your_password"
                    },
                    "response": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            }
        },
        
        "endpoints": {
            "authentication": {
                "register": {
                    "url": f"{base_url}api/auth/users/",
                    "method": "POST",
                    "description": "Register a new user",
                    "body": {
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "password": "secure_password",
                        "re_password": "secure_password"
                    }
                },
                "login": {
                    "url": f"{base_url}api/auth/jwt/create/",
                    "method": "POST",
                    "description": "Login and get JWT tokens"
                },
                "refresh": {
                    "url": f"{base_url}api/auth/jwt/refresh/",
                    "method": "POST",
                    "description": "Refresh JWT access token"
                },
                "logout": {
                    "url": f"{base_url}api/auth/jwt/logout/",
                    "method": "POST",
                    "description": "Logout and blacklist refresh token"
                }
            },
            
            "products": {
                "list_products": {
                    "url": f"{base_url}api/products/",
                    "method": "GET",
                    "description": "Get paginated list of products",
                    "query_params": {
                        "search": "Search products by title",
                        "category": "Filter by category ID",
                        "page": "Page number for pagination",
                        "page_size": "Number of items per page"
                    },
                    "example": f"{base_url}api/products/?search=running&page=1"
                },
                "product_detail": {
                    "url": f"{base_url}api/products/{{product_id}}/",
                    "method": "GET",
                    "description": "Get detailed information about a specific product"
                }
            },
            
            "cart": {
                "get_cart": {
                    "url": f"{base_url}api/cart/",
                    "method": "GET",
                    "description": "Get user's shopping cart",
                    "authentication": "Required"
                },
                "add_to_cart": {
                    "url": f"{base_url}api/cart/add/",
                    "method": "POST",
                    "description": "Add product to cart",
                    "authentication": "Required",
                    "body": {
                        "product_id": "UUID of the product",
                        "variant_id": "UUID of the variant (optional)",
                        "quantity": "Number of items to add"
                    }
                },
                "update_cart_item": {
                    "url": f"{base_url}api/cart/items/{{item_id}}/",
                    "method": "PATCH",
                    "description": "Update quantity of cart item",
                    "authentication": "Required",
                    "body": {
                        "quantity": "New quantity"
                    }
                },
                "remove_cart_item": {
                    "url": f"{base_url}api/cart/items/{{item_id}}/",
                    "method": "DELETE",
                    "description": "Remove item from cart",
                    "authentication": "Required"
                },
                "clear_cart": {
                    "url": f"{base_url}api/cart/clear/",
                    "method": "POST",
                    "description": "Clear all items from cart",
                    "authentication": "Required"
                }
            },
            
            "orders": {
                "create_order": {
                    "url": f"{base_url}api/orders/",
                    "method": "POST",
                    "description": "Create order from cart",
                    "authentication": "Required",
                    "body": {
                        "shipping_address_id": "UUID of shipping address",
                        "billing_address_id": "UUID of billing address",
                        "payment_method": "Payment method (optional)"
                    }
                },
                "list_orders": {
                    "url": f"{base_url}api/orders/",
                    "method": "GET",
                    "description": "Get user's orders",
                    "authentication": "Required"
                },
                "order_detail": {
                    "url": f"{base_url}api/orders/{{order_id}}/",
                    "method": "GET",
                    "description": "Get detailed order information",
                    "authentication": "Required"
                },
                "cancel_order": {
                    "url": f"{base_url}api/orders/{{order_id}}/cancel/",
                    "method": "POST",
                    "description": "Cancel an order",
                    "authentication": "Required"
                }
            }
        },
        
        "status_codes": {
            "200": "OK - Request successful",
            "201": "Created - Resource created successfully",
            "400": "Bad Request - Invalid request data",
            "401": "Unauthorized - Authentication required",
            "403": "Forbidden - Insufficient permissions",
            "404": "Not Found - Resource not found",
            "500": "Internal Server Error - Server error"
        },
        
        "order_statuses": {
            "pending": "Order is pending confirmation",
            "confirmed": "Order has been confirmed",
            "processing": "Order is being processed",
            "shipped": "Order has been shipped",
            "delivered": "Order has been delivered",
            "cancelled": "Order has been cancelled",
            "refunded": "Order has been refunded"
        },
        
        "examples": {
            "complete_flow": {
                "description": "Complete shopping flow example",
                "steps": [
                    "1. Register: POST /api/auth/users/",
                    "2. Login: POST /api/auth/jwt/create/",
                    "3. Browse products: GET /api/products/",
                    "4. Add to cart: POST /api/cart/add/",
                    "5. View cart: GET /api/cart/",
                    "6. Create order: POST /api/orders/",
                    "7. Track order: GET /api/orders/{order_id}/"
                ]
            }
        },
        
        "links": {
            "swagger_ui": f"{base_url}api/docs/",
            "schema": f"{base_url}api/schema/",
            "admin": f"{base_url}admin/"
        }
    }
    
    return Response(documentation)


def api_landing(request):
    """
    Landing page for the API
    """
    return render(request, 'api_landing.html')

# E-commerce API

A comprehensive e-commerce backend API built with Django REST Framework.

## 🚀 Quick Start

1. **Visit the API**: http://127.0.0.1:8000/
2. **API Root**: http://127.0.0.1:8000/api/
3. **Documentation**: http://127.0.0.1:8000/api/documentation/
4. **Swagger UI**: http://127.0.0.1:8000/api/docs/
5. **Admin Panel**: http://127.0.0.1:8000/admin/

## 📋 API Endpoints

### Authentication

- `POST /api/auth/users/` - Register new user
- `POST /api/auth/jwt/create/` - Login (get JWT token)
- `POST /api/auth/jwt/refresh/` - Refresh JWT token
- `POST /api/auth/jwt/logout/` - Logout
- `GET /api/auth/users/me/` - Get current user profile

### Products

- `GET /api/products/` - List products (with pagination, search, filtering)
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/{id}/variants/` - Get product variants
- `GET /api/products/{id}/images/` - Get product images

### Categories

- `GET /api/categories/` - List categories
- `GET /api/categories/{id}/` - Get category details
- `GET /api/categories/{id}/products/` - Get category products

### Shopping Cart

- `GET /api/cart/` - Get user's cart
- `POST /api/cart/add/` - Add item to cart
- `GET /api/cart/items/` - List cart items
- `PATCH /api/cart/items/{id}/` - Update cart item quantity
- `DELETE /api/cart/items/{id}/` - Remove cart item
- `POST /api/cart/clear/` - Clear cart
- `GET /api/cart/summary/` - Get cart summary

### Orders

- `GET /api/orders/` - List user's orders
- `POST /api/orders/` - Create order from cart
- `GET /api/orders/{id}/` - Get order details
- `POST /api/orders/{id}/cancel/` - Cancel order
- `GET /api/orders/statistics/` - Get order statistics

### Users

- `GET /api/users/` - List users (admin)
- `GET /api/users/{id}/` - Get user details
- `GET /api/users/{id}/addresses/` - Get user addresses
- `GET /api/users/{id}/orders/` - Get user orders (admin)

### Admin Only

- `PATCH /api/orders/{id}/status/` - Update order status

## 🔐 Authentication

This API uses JWT (JSON Web Token) authentication:

1. **Register**: `POST /api/auth/users/`
2. **Login**: `POST /api/auth/jwt/create/`
3. **Include token**: `Authorization: Bearer <your_token>`

### Example Login Request

```json
POST /api/auth/jwt/create/
{
    "email": "user@example.com",
    "password": "your_password"
}
```

### Example Response

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 🛒 Complete Shopping Flow

1. **Register**: `POST /api/auth/users/`
2. **Login**: `POST /api/auth/jwt/create/`
3. **Browse Products**: `GET /api/products/`
4. **Add to Cart**: `POST /api/cart/add/`
5. **View Cart**: `GET /api/cart/`
6. **Create Order**: `POST /api/orders/`
7. **Track Order**: `GET /api/orders/{order_id}/`

## 📊 Order Statuses

- `pending` - Order is pending confirmation
- `confirmed` - Order has been confirmed
- `processing` - Order is being processed
- `shipped` - Order has been shipped
- `delivered` - Order has been delivered
- `cancelled` - Order has been cancelled
- `refunded` - Order has been refunded

## 🔧 Features

- ✅ JWT Authentication
- ✅ Product Catalog with Categories & Variants
- ✅ Shopping Cart Management
- ✅ Order Processing with Status Tracking
- ✅ User Management & Addresses
- ✅ Stock Management
- ✅ Admin Interface
- ✅ API Documentation (Swagger)
- ✅ Pagination & Filtering
- ✅ Search Functionality

## 📝 Example Requests

### Add Product to Cart

```json
POST /api/cart/add/
{
    "product_id": "uuid-of-product",
    "variant_id": "uuid-of-variant",
    "quantity": 2
}
```

### Create Order

```json
POST /api/orders/
{
    "shipping_address_id": "uuid-of-address",
    "billing_address_id": "uuid-of-address",
    "payment_method": "credit_card"
}
```

### Search Products

```
GET /api/products/?search=running&page=1&page_size=10
```

## 🛠️ Development

### Running the Server

```bash
# Activate virtual environment
venv\Scripts\activate

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Creating Superuser

```bash
python manage.py createsuperuser
```

## 📚 Additional Resources

- **API Root**: http://127.0.0.1:8000/api/
- **Detailed Documentation**: http://127.0.0.1:8000/api/documentation/
- **Interactive Swagger UI**: http://127.0.0.1:8000/api/docs/
- **Django Admin**: http://127.0.0.1:8000/admin/

---

Built with ❤️ using Django REST Framework

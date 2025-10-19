from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid
from decimal import Decimal
from Product.models import Product, Variant
from User.models import Address


class Order(models.Model):
    """Order model representing a customer's purchase"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Order details
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Shipping information
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='shipping_orders')
    billing_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='billing_orders')
    
    # Payment information (will be linked to Payment app later)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number} - {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        """Generate a unique order number"""
        import time
        timestamp = str(int(time.time()))[-8:]  # Last 8 digits of timestamp
        return f"ORD{timestamp}"

    @property
    def total_items(self):
        """Total number of items in this order"""
        return sum(item.quantity for item in self.items.all())

    def calculate_totals(self):
        """Calculate order totals"""
        self.subtotal = sum(item.total_price for item in self.items.all())
        # For now, we'll keep tax and shipping simple
        # In a real application, these would be calculated based on business rules
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost

    def can_be_cancelled(self):
        """Check if order can be cancelled"""
        return self.status in [self.Status.PENDING, self.Status.CONFIRMED]

    def cancel(self):
        """Cancel the order and restore stock"""
        if not self.can_be_cancelled():
            raise ValidationError("Order cannot be cancelled in its current status")
        
        # Restore stock for all items
        for item in self.items.all():
            item.restore_stock()
        
        self.status = self.Status.CANCELLED
        self.save()

    def confirm(self):
        """Confirm the order"""
        if self.status != self.Status.PENDING:
            raise ValidationError("Only pending orders can be confirmed")
        
        # Validate stock availability before confirming
        for item in self.items.all():
            if not item.is_stock_available():
                raise ValidationError(f"Insufficient stock for {item.product.title}")
        
        # Reserve stock
        for item in self.items.all():
            item.reserve_stock()
        
        self.status = self.Status.CONFIRMED
        self.confirmed_at = models.DateTimeField(auto_now=True)
        self.save()


class OrderItem(models.Model):
    """Individual item within an order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        variant_str = f" - {self.variant.name}" if self.variant else ""
        return f"{self.product.title}{variant_str} x{self.quantity}"

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def get_unit_price(self):
        """Get the unit price (from variant if available, otherwise product price)"""
        if self.variant:
            return self.variant.get_price()
        return self.product.price

    def is_stock_available(self):
        """Check if sufficient stock is available"""
        available_stock = self.variant.stock if self.variant else self.product.stock
        return self.quantity <= available_stock

    def reserve_stock(self):
        """Reserve stock for this order item"""
        if self.variant:
            if self.variant.stock < self.quantity:
                raise ValidationError(f"Insufficient stock for variant {self.variant.name}")
            self.variant.stock -= self.quantity
            self.variant.save()
        else:
            if self.product.stock < self.quantity:
                raise ValidationError(f"Insufficient stock for product {self.product.title}")
            self.product.stock -= self.quantity
            self.product.save()

    def restore_stock(self):
        """Restore stock when order is cancelled"""
        if self.variant:
            self.variant.stock += self.quantity
            self.variant.save()
        else:
            self.product.stock += self.quantity
            self.product.save()


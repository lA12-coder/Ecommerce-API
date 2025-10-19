from django.db import models
from django.conf import settings
import uuid
from Product.models import Product, Variant


class Cart(models.Model):
    """Shopping cart for a user"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.email}"

    @property
    def total_items(self):
        """Total number of items in cart"""
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """Total price of all items in cart"""
        return sum(item.total_price for item in self.items.all())

    def clear(self):
        """Clear all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """Individual item in a shopping cart"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['cart', 'product', 'variant']

    def __str__(self):
        variant_str = f" - {self.variant.name}" if self.variant else ""
        return f"{self.product.title}{variant_str} x{self.quantity}"

    @property
    def unit_price(self):
        """Get the unit price (from variant if available, otherwise product price)"""
        if self.variant:
            return self.variant.get_price()
        return self.product.price

    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return self.unit_price * self.quantity

    def clean(self):
        """Validate cart item"""
        from django.core.exceptions import ValidationError
        
        # Check if variant belongs to the product
        if self.variant and self.variant.product != self.product:
            raise ValidationError("Variant must belong to the selected product")
        
        # Check stock availability
        available_stock = self.variant.stock if self.variant else self.product.stock
        if self.quantity > available_stock:
            raise ValidationError(f"Not enough stock. Available: {available_stock}")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

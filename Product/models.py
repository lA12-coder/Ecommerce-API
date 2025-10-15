from attr.validators import max_len
from django.db import models
import uuid
from django.utils.text import slugify


# Category db model
class Category(models.Model):
    id = models.UUIDField(
        verbose_name="ID",
        help_text="ID for Categories",
        editable=False,
        default=uuid.uuid4(),
        primary_key=True,
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name='children')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:200]
            slug = base
            idx = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base}-{idx}"
                idx += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

#Product db model
class Product(models.Model):
    id = models.UUIDField(
        verbose_name="product_id",
        help_text="ID for products",
        editable=False,
        default=uuid.uuid4(),
        primary_key=True,
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280 ,unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField("Price of a Product", max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=20, default="USD")
    sku = models.CharField(max_length=120, unique=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ManyToManyField(Category , related_name='categories')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200]
            slug = base
            idx = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{idx}"
                idx += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

#variant db model
class Variant(models.Model):
    """
    product variant eg: size/color.
    Each variant has its own SKU and stock.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), verbose_name='variant_id', editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=100, help_text="eg. 'size L / Red' ")
    sku = models.CharField(max_length=120, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Optional price override; if blank, product.price is used")
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def get_price(self):
        return self.price if self.price is not None else self.product.price

    def __str__(self):
        return f"{self.product.titile} - {self.name}"

class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), verbose_name='variant_id', editable=False)
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/%Y/%m/%d/", )
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return f"Image for {self.product.title} ({self.pk})"






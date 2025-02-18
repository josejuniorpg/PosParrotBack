from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel

from apps.customers.models import Customer
from apps.restaurants.models import Table


class Order(TimeStampedModel):
    """
    Represents an order placed in the restaurant.
    """
    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Processing'),
        (2, 'Completed'),
        (3, 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        (0, 'Cash'),
        (1, 'Credit Card'),
        (2, 'Debit Card'),
        (3, 'Mobile Payment'),
        (4, 'Bank Transfer'),
        (5, 'Voucher'),
    ]

    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name="orders",
                                   verbose_name="Restaurant")
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders",
                                 verbose_name="Customer")
    tables = models.ManyToManyField(Table, related_name="orders", verbose_name="Tables")
    employee = models.ForeignKey('restaurants.Employee', on_delete=models.CASCADE, related_name="orders",
                                 verbose_name="Employee")
    customer_name = models.CharField(max_length=255, blank=True, verbose_name="Customer Name (if anonymous)")
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.SmallIntegerField(choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - Tables {[table.table_number for table in self.tables.all()]} - {self.get_status_display()}"


class Category(TimeStampedModel):
    """
    Represents a product category. The categories are shared among All User.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    status = models.BooleanField(default=True, verbose_name="Status")

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """
    Represents a product in the restaurant.
    """
    restaurants = models.ManyToManyField('restaurants.Restaurant', related_name="products",
                                         verbose_name="Restaurants")
    name = models.CharField(max_length=255, verbose_name="Product Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    image = models.ImageField(blank=True, null=True, verbose_name="Product Image")
    status = models.SmallIntegerField(choices=[(0, 'Available'), (1, 'Out of Stock')], default=0)
    categories = models.ManyToManyField(Category, related_name="products", verbose_name="Categories")

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"


class OrderProduct(models.Model):
    """
    Represents the products in an order, tracking quantity.
    """
    order = models.ForeignKey('pos_systems.Order', on_delete=models.CASCADE, related_name="order_products",
                              verbose_name="Order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_products",
                                verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    class Meta:
        unique_together = ('order', 'product')

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError({"quantity": "Quantity must be greater than 0."})

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name} x{self.quantity}"

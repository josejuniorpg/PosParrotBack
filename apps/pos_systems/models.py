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

    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name="orders", verbose_name="Restaurant")
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders", verbose_name="Customer")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="orders", verbose_name="Table")
    employee = models.ForeignKey('restaurants.Employee', on_delete=models.CASCADE, related_name="orders", verbose_name="Employee")
    customer_name = models.CharField(max_length=255, blank=True, verbose_name="Customer Name (if anonymous)")
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.SmallIntegerField(choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - Table {self.table.table_number} - {self.get_status_display()}"

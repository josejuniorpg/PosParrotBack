from django.db import models
from model_utils.models import TimeStampedModel


class Customer(TimeStampedModel):
    """
    Represents a customer.
    """
    name = models.CharField(max_length=255, verbose_name="Customer Name")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="Email")

    def __str__(self):
        return self.name if self.name else "Anonymous Customer"

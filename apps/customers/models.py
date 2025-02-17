from django.db import models
from model_utils.models import TimeStampedModel

from django.db import models
from model_utils.models import TimeStampedModel


class Customer(TimeStampedModel):
    """
    Represents a customer belonging to a specific restaurant.
    """
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE,
        related_name="customers",
        verbose_name="Restaurant"
    )
    name = models.CharField(max_length=255, verbose_name="Customer Name")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="Email")

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

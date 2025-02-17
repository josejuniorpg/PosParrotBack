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
    email = models.EmailField(null=True, blank=True, verbose_name="Email")  # ✅ No es único globalmente

    class Meta:
        # This constraint ensures that the email is unique per restaurant, not globally
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'email'], name="unique_customer_email_per_restaurant")
        ]

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

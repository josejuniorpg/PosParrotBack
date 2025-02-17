from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel


class Restaurant(TimeStampedModel):
    """
    Represents a restaurant owned by a user in the system.

    Attributes:
        user (User): The owner of the restaurant.
        name (str): The name of the restaurant.
        address (str): The physical address of the restaurant.
        phone_number (str): The contact phone number.
        created (datetime): The timestamp when the record was created.
        modified (datetime): The timestamp when the record was last updated.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurants")
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Employee(TimeStampedModel):
    """
    Represents an employee working at a restaurant, such as a waiter, manager, or chef.

    Attributes:
        restaurant (Restaurant): The restaurant where the employee works.
        email (str): The unique email address of the employee.
        role (str): The employee's role within the restaurant ('Manager', 'Waiter', 'Chef').
        created (datetime): The timestamp when the record was created.
        modified (datetime): The timestamp when the record was last updated.
    """
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Waiter', 'Waiter'),
        ('Chef', 'Chef'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="employees",
                                   verbose_name="Restaurant Name")
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(upload_to='restaurants/employees/', null=True, blank=True)

    def __str__(self):
        return f"{self.role} - {self.email}"


class Table(TimeStampedModel):
    """
    Represents a restaurant table.
    """
    STATUS_CHOICES = [
        (0, 'Available'),
        (1, 'Busy'),
    ]

    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE,
        related_name="tables",
        verbose_name="Restaurant"
    )
    table_number = models.PositiveIntegerField(verbose_name="Table Number")
    capacity = models.PositiveIntegerField(verbose_name="Capacity")
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return f"Table {self.table_number} - {self.get_status_display()} ({self.restaurant.name})"

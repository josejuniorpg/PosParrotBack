from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Customers.
    """
    list_display = ('name', 'email', 'created',)
    search_fields = ('name', 'email',)
    ordering = ('created', 'name', 'email',)

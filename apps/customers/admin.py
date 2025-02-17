from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Customers.
    """
    list_display = ('name', 'email', 'restaurant', 'created')
    list_filter = ('restaurant',)
    search_fields = ('name', 'email', 'restaurant__name')
    ordering = ('created',)

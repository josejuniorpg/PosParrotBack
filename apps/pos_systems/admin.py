from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Orders.
    """
    list_display = ('id', 'restaurant', 'status', 'total', 'payment_method', 'created')
    list_filter = ('status', 'payment_method', 'restaurant')
    search_fields = ('customer_name', 'restaurant__name')
    ordering = ('-created',)
    filter_horizontal = ('tables',)  # ✅ Permite seleccionar múltiples mesas en el admin



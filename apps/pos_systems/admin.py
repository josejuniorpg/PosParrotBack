from django.contrib import admin
from .models import Order, Category, Product, OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Orders.
    """
    list_display = ('id', 'restaurant', 'status', 'total', 'payment_method', 'created')
    list_filter = ('status', 'payment_method', 'restaurant')
    search_fields = ('customer_name', 'restaurant__name')
    ordering = ('-created',)
    filter_horizontal = ('tables',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created')
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Products.
    """
    list_display = ('name', 'price', 'status', 'get_categories', 'created')
    search_fields = ('name',)
    list_filter = ('status', 'categories__name')

    def get_categories(self, obj):
        """Return categories as a comma-separated string."""
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = "Categories"


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__id', 'product__name')

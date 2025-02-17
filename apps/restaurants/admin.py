from django.contrib import admin

from .models import Employee, Restaurant, Table


class RestaurantFilter(admin.SimpleListFilter):
    """
    Custom filter to display restaurants by name in the Django admin.
    """
    title = "Restaurant"  # ✅ Custom label shown in the filter section
    parameter_name = "restaurant"

    def lookups(self, request, model_admin):
        """Defines the choices in the filter dropdown."""
        restaurants = set(Employee.objects.values_list('restaurant__id', 'restaurant__name'))
        return [(r[0], r[1]) for r in restaurants]

    def queryset(self, request, queryset):
        """Filters the queryset based on the selected value."""
        if self.value():
            return queryset.filter(restaurant__id=self.value())
        return queryset


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Restaurant.
    """
    list_display = ('name', 'user', 'phone_number', 'created', 'modified',)
    search_fields = ('name', 'user__email', 'phone_number',)
    list_filter = ('created', 'modified',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'restaurant', 'created', 'modified')
    search_fields = ('email', 'restaurant__name')
    list_filter = ('role', RestaurantFilter)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin, admin.SimpleListFilter):
    """
    Admin panel configuration for Tables.
    """

    list_display = ('restaurant', 'table_number', 'capacity', 'status', 'modified')
    list_filter = ('status', 'restaurant__name',)
    search_fields = ('table_number', 'restaurant__name')

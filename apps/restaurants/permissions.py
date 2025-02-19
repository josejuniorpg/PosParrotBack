from rest_framework.permissions import BasePermission

from apps.restaurants.models import Restaurant


class IsRestaurantOwner(BasePermission):
    """
    Allows access only to restaurant owners or superusers.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_superuser or Restaurant.objects.filter(user=request.user).exists()
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.restaurant.user == request.user

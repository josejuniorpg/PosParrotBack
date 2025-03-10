from rest_framework import pagination, viewsets
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Employee, Restaurant, Table
from .permissions import IsRestaurantOwner
from .serializers import (EmployeeSerializer, RestaurantSerializer,
                          TableSerializer)


class EmployeePagination(pagination.PageNumberPagination):
    """ Custom pagination class for Employees. """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Restaurants.
    Supports CRUD operations (list, create, retrieve, update, delete).
    """
    queryset = Restaurant.objects.filter()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        """Only return the restaurants that the user owns."""
        if self.request.user.is_superuser:
            return Restaurant.objects.all()
        return Restaurant.objects.filter(user=self.request.user)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Employees.
    Supports CRUD operations (list, create, retrieve, update, delete).
    """
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePagination
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        """Return only employees that belong to the specified restaurant in query parameters."""
        if self.request.user.is_superuser:
            return Employee.objects.all()

        restaurant_id = self.request.query_params.get("restaurant")

        if restaurant_id:
            if not Restaurant.objects.filter(id=restaurant_id, user=self.request.user).exists():
                raise PermissionDenied("You are not the owner of this restaurant.")
            return Employee.objects.filter(restaurant_id=restaurant_id)

        return Employee.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the employee is created only in the specified restaurant."""
        restaurant_id = self.request.data.get("restaurant")

        if not restaurant_id:
            raise ValidationError("A restaurant ID is required.")

        restaurant = Restaurant.objects.filter(id=restaurant_id, user=self.request.user).first()
        if not restaurant:
            raise ValidationError("You do not have permission to add employees to this restaurant.")

        serializer.save(restaurant=restaurant)


class TableViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing restaurant tables.
    """
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        """Return only tables that belong to the specified restaurant in query parameters."""
        if self.request.user.is_superuser:
            return Table.objects.all()

        restaurant_id = self.request.query_params.get("restaurant")

        if restaurant_id:
            if not Restaurant.objects.filter(id=restaurant_id, user=self.request.user).exists():
                raise PermissionDenied("You are not the owner of this restaurant.")
            return Table.objects.filter(restaurant_id=restaurant_id)

        return Table.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the table is created only in the specified restaurant."""
        restaurant_id = self.request.data.get("restaurant")

        if not restaurant_id:
            raise ValidationError("A restaurant ID is required.")

        restaurant = Restaurant.objects.filter(id=restaurant_id, user=self.request.user).first()
        if not restaurant:
            raise PermissionDenied("You do not have permission to add tables to this restaurant.")

        serializer.save(restaurant=restaurant)

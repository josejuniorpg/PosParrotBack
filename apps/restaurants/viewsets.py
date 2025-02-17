from rest_framework import pagination, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Employee, Restaurant, Table
from .serializers import (EmployeeSerializer, RestaurantSerializer,
                          TableSerializer)


class IsAdminOrOwnerPermission(IsAuthenticated):
    """
    Custom permission to allow only admins or restaurant owners to access the list.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser or Restaurant.objects.filter(user=request.user).exists()

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

    def get_queryset(self):
        """Only return the restaurants that the user owns."""
        if self.request.user.is_superuser:
            return Restaurant.objects.all()
        return Restaurant.objects.filter(user=self.request.user)

    def get_permissions(self):
        """Only allow access to list for admins or restaurant owners."""
        if self.action == 'list':
            return [IsAdminOrOwnerPermission()]
        return [IsAuthenticated()]



class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Employees.
    Supports CRUD operations (list, create, retrieve, update, delete).
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePagination


    def get_queryset(self):
        """Only return the employees that the user owns."""
        if self.request.user.is_superuser:
            return Employee.objects.all()
        return Employee.objects.filter(restaurant__user=self.request.user)

    def get_permissions(self):
        """Only allow access to list for admins or restaurant owners."""
        if self.action == 'list':
            return [IsAdminOrOwnerPermission()]
        return [IsAuthenticated()]


class TableViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing restaurant tables.
    """
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return the tables that the user owns."""
        if self.request.user.is_superuser:
            return Table.objects.all()
        return Table.objects.filter(restaurant__user=self.request.user)

    def get_permissions(self):
        """Only allow access to list for admins or restaurant owners."""
        if self.action == 'list':
            return [IsAdminOrOwnerPermission()]
        return [IsAuthenticated()]
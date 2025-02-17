from rest_framework import viewsets
from .models import Restaurant, Employee
from .serializers import RestaurantSerializer, EmployeeSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Restaurants.
    Supports CRUD operations (list, create, retrieve, update, delete).
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Employees.
    Supports CRUD operations (list, create, retrieve, update, delete).
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

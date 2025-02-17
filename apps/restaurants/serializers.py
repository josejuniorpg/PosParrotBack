from rest_framework import serializers
from .models import Restaurant, Employee

class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant model.
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'created', 'modified']


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee model.
    """

    class Meta:
        model = Employee
        fields = ['id', 'restaurant', 'email', 'role', 'profile_picture', 'created', 'modified']

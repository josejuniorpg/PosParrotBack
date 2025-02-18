from rest_framework import serializers

from .models import Employee, Restaurant, Table


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant model.
    """

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'created', 'modified']


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee model with email validation.
    """
    class Meta:
        model = Employee
        fields = ['id', 'name','restaurant', 'email', 'role', 'profile_picture', 'created', 'modified']

    def validate_email(self, value):
        """Ensure email is unique within the same restaurant."""
        restaurant = self.initial_data.get('restaurant')  # ✅ Obtener el restaurante desde la solicitud
        employee_id = self.instance.id if self.instance else None  # ✅ Obtener el ID si está editando

        if Employee.objects.filter(restaurant=restaurant, email=value).exclude(id=employee_id).exists():
            raise serializers.ValidationError("This email is already in use in this restaurant.")

        return value

class TableSerializer(serializers.ModelSerializer):
    """
    Serializer for Table model with validation.
    """

    class Meta:
        model = Table
        fields = ['id', 'table_number', 'capacity', 'status', 'created', 'modified']

    def validate(self, data):
        """Ensure table_number is unique within the same restaurant."""
        restaurant = data.get('restaurant')
        table_number = data.get('table_number')

        if Table.objects.filter(restaurant=restaurant, table_number=table_number).exists():
            raise serializers.ValidationError({"table_number": "This table number already exists in this restaurant."})

        return data

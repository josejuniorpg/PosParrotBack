from django import forms

from .models import Employee, Restaurant


class RestaurantForm(forms.ModelForm):
    """
    Form for creating and updating a Restaurant.
    """
    class Meta:
        model = Restaurant
        fields = ['user', 'name', 'address', 'phone_number']

class EmployeeForm(forms.ModelForm):
    """
    Form for creating and updating an Employee.
    """
    class Meta:
        model = Employee
        fields = ['restaurant', 'email', 'role', 'profile_picture']

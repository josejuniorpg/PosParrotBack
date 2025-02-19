from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model with email uniqueness validation per restaurant.
    """
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'restaurant']

    def validate_email(self, value):
        """
        Ensure the email is unique per restaurant.
        """
        restaurant_id = self.context['request'].query_params.get("restaurant")
        if restaurant_id and Customer.objects.filter(email=value, restaurant_id=restaurant_id).exists():
            raise serializers.ValidationError("A customer with this email already exists in this restaurant.")
        return value
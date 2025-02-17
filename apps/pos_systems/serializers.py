from rest_framework import serializers
from .models import Order
from ..restaurants.models import Table


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    tables = serializers.PrimaryKeyRelatedField(many=True, queryset=Table.objects.all())  # ✅ Soporte ManyToMany

    class Meta:
        model = Order
        fields = [
            'id', 'restaurant', 'customer', 'tables', 'employee', 'customer_name',
            'status', 'subtotal', 'discount', 'tax', 'tips', 'total', 'payment_method',
            'created', 'modified'
        ]

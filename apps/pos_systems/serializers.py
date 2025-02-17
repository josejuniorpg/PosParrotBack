from rest_framework import serializers
from ..restaurants.models import Table, Restaurant
from .models import Order, Category, Product, OrderProduct


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


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'status', ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    categories = serializers.PrimaryKeyRelatedField(many=True,
                                                    queryset=Category.objects.all())
    restaurants = serializers.PrimaryKeyRelatedField(many=True, queryset=Restaurant.objects.all())

    class Meta:
        model = Product
        fields = ['id','restaurants' ,'name', 'price', 'image', 'status', 'categories', 'created', 'modified']


class OrderProductSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderProduct model.
    """

    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'quantity']

from rest_framework import serializers
from ..restaurants.models import Table, Restaurant
from .models import Order, Category, Product, OrderProduct


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model with additional validation.
    """

    class Meta:
        model = Order
        fields = [
            'id', 'restaurant', 'customer', 'tables', 'employee', 'customer_name',
            'status', 'subtotal', 'discount', 'tax', 'tips', 'total', 'payment_method',
        ]

    def validate(self, data):
        """Ensure product belongs to the restaurant of the order and is available."""
        restaurant = data.get('restaurant')
        order_products = data.get('order_products', [])

        for item in order_products:
            product = item['product']
            if product not in restaurant.products.all():
                raise serializers.ValidationError("One or more products do not belong to the restaurant of this order.")
            if product.status != 0:
                raise serializers.ValidationError(f"The product '{product.name}' is not available for ordering.")

        # Validate totals
        subtotal = data.get('subtotal', 0)
        tax = data.get('tax', 0) or 0
        discount = data.get('discount', 0) or 0
        tips = data.get('tips', 0) or 0
        total = data.get('total', 0)

        calculated_total = subtotal + tax - discount + tips
        if round(calculated_total, 2) != round(total, 2):
            raise serializers.ValidationError("Total amount is incorrect based on subtotal, tax, discount, and tips.")

        return data


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'status', ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model with image upload support.
    """
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    restaurants = serializers.PrimaryKeyRelatedField(many=True, queryset=Restaurant.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'restaurants', 'name', 'price', 'image', 'status', 'categories', ]

    def validate_name(self, value):
        """
        Ensure product name is unique within the assigned restaurants.
        """
        request = self.context.get('request')
        if not request:
            return value  # Skip validation if request is not available

        restaurant_ids = request.data.get("restaurants", [])
        if not restaurant_ids:
            raise serializers.ValidationError("At least one restaurant must be assigned to the product.")

        if Product.objects.filter(name=value, restaurants__id__in=restaurant_ids).exists():
            raise serializers.ValidationError(
                "A product with this name already exists in one of the selected restaurants.")

        return value


class OrderProductSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderProduct model with validation.
    """

    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'quantity']

    @staticmethod
    def validate_quantity(value):
        """Ensure quantity is greater than zero."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        """Ensure product belongs to the restaurant of the order and is available."""
        order = data.get('order')
        product = data.get('product')

        if product not in order.restaurant.products.all():
            raise serializers.ValidationError("The selected product does not belong to the restaurant of this order.")

        if product.status != 0:  # 0 = Available
            raise serializers.ValidationError(f"The product '{product.name}' is not available for ordering.")

        return data

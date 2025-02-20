from rest_framework import pagination, viewsets, serializers
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from ..customers.models import Customer
from ..restaurants.models import Restaurant, Employee, Table
from .models import Order, Category, Product, OrderProduct
from .serializers import OrderSerializer, CategorySerializer, ProductSerializer, OrderProductSerializer
from ..restaurants.permissions import IsRestaurantOwner


class ProductPagination(PageNumberPagination):
    """
    Pagination for Customers.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class OrderPagination(pagination.PageNumberPagination):
    """
    Custom pagination for Customers.
    """
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination

    def get_queryset(self):
        """Only return orders belonging to the authenticated user's restaurant."""
        if self.request.user.is_superuser:
            return Order.objects.all()

        restaurant_id = self.request.query_params.get("restaurant")
        if restaurant_id:
            if not Restaurant.objects.filter(id=restaurant_id, user=self.request.user).exists():
                raise PermissionDenied("You are not the owner of this restaurant.")
            return Order.objects.filter(restaurant_id=restaurant_id)

        return Order.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the order is created only in the user's restaurant and validate consistency."""
        restaurant_id = self.request.data.get("restaurant")

        if not restaurant_id:
            raise ValidationError("A restaurant ID is required to create an order.")

        restaurant = Restaurant.objects.filter(id=restaurant_id, user=self.request.user).first()
        if not restaurant:
            raise PermissionDenied("You do not have permission to create orders in this restaurant.")

        # Validate that the table exists and is available
        table_ids = self.request.data.get("tables", [])
        for table_id in table_ids:
            table = Table.objects.filter(table_number=table_id, restaurant=restaurant).first()
            if not table:
                raise ValidationError(f"Table {table_id} does not exist or does not belong to this restaurant.")

        # Validate that the employee belongs to the restaurant
        employee_id = self.request.data.get("employee")
        if employee_id:
            if not Employee.objects.filter(id=employee_id, restaurant=restaurant).exists():
                raise ValidationError("The assigned employee does not belong to this restaurant.")

        # Validate that the customer belongs to the restaurant
        customer_id = self.request.data.get("customer")
        if customer_id:
            if not Customer.objects.filter(id=customer_id, restaurant=restaurant).exists():
                raise ValidationError("The assigned customer does not belong to this restaurant.")

        serializer.save(restaurant=restaurant)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product categories.
    Only active categories (status = 0) are returned.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        """Return only active categories."""
        return Category.objects.filter(status=1)

    def perform_create(self, serializer):
        """Only the Superuser, and Staff  can create a category."""
        if not self.request.user.is_staff:
            raise PermissionDenied("You are not authorized to create a category.")
        serializer.save()


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProductPagination
    parser_classes = [MultiPartParser, FormParser]  # Enable file uploads

    def get_queryset(self):
        """
        Only return products for the authenticated user's restaurants.
        """
        if self.request.user.is_superuser:
            return Product.objects.all()

        restaurant_id = self.request.query_params.get("restaurant")

        if restaurant_id:
            if not Restaurant.objects.filter(id=restaurant_id, user=self.request.user).exists():
                raise PermissionDenied("You are not the owner of this restaurant.")
            return Product.objects.filter(restaurants__id=restaurant_id)

        return Product.objects.filter(restaurants__user=self.request.user).distinct()

    def perform_create(self, serializer):
        """
        Ensure that a product can only be assigned to restaurants owned by the same user.
        Also, prevent duplicate product names within the same restaurant.
        """
        user_restaurants = Restaurant.objects.filter(user=self.request.user)
        selected_restaurants = serializer.validated_data.get("restaurants")
        product_name = serializer.validated_data.get("name")

        if not set(selected_restaurants).issubset(set(user_restaurants)):
            raise serializers.ValidationError("You can only assign products to your own restaurants.")
        serializer.save()

    @staticmethod
    def has_permission(request, view):
        """Custom permission to allow only admins or restaurant owners to access the list."""
        return request.user.is_superuser or Restaurant.objects.filter(user=request.user).exists()


class OrderProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products in an order.
    """
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return order products filtered by a specific order if provided."""
        if self.request.user.is_superuser:
            return OrderProduct.objects.all()

        order_id = self.request.query_params.get("order")
        if order_id:
            order = Order.objects.filter(id=order_id, restaurant__user=self.request.user).first()
            if not order:
                raise PermissionDenied("You do not have access to this order.")
            return OrderProduct.objects.filter(order=order)

        return OrderProduct.objects.filter(order__restaurant__user=self.request.user)
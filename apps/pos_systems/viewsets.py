from rest_framework import pagination, viewsets, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from ..restaurants.models import Restaurant
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
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination

    def get_queryset(self):
        """Only return orders belonging to the authenticated user's restaurant."""
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(restaurant__user=self.request.user)

    @staticmethod
    def has_permission(request, view):
        """Custom permission to allow only admins or restaurant owners to access the list."""
        return request.user.is_superuser or Restaurant.objects.filter(user=request.user).exists()


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

        # Prevent duplicate product names within the same restaurant
        for restaurant in selected_restaurants:
            if Product.objects.filter(name=product_name, restaurants=restaurant).exists():
                raise serializers.ValidationError(
                    f"A product with the name '{product_name}' already exists in {restaurant.name}.")

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
    queryset = OrderProduct.objects.all()
    permission_classes = [IsAuthenticated]

    @staticmethod
    def has_permission(request, view):
        """Custom permission to allow only admins or restaurant owners to access the list."""
        return request.user.is_superuser or Restaurant.objects.filter(user=request.user).exists()

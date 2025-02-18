from rest_framework import pagination, viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from ..restaurants.models import Restaurant
from .models import Order, Category, Product, OrderProduct
from .serializers import OrderSerializer, CategorySerializer, ProductSerializer, OrderProductSerializer


class OrderPagination(pagination.PageNumberPagination):
    """
    Custom pagination for Customers.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


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
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return all categories.
        """
        return Category.objects.all()

    @staticmethod
    def has_permission(request, view):
        """Custom permission to allow only admins or restaurant owners to access the list."""
        return request.user.is_superuser or Restaurant.objects.filter(user=request.user).exists()


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Only return products for the authenticated user's restaurants.
        """
        if self.request.user.is_superuser:
            return Product.objects.all()

        return Product.objects.filter(restaurants__user=self.request.user).distinct()

    def perform_create(self, serializer):
        """
        Ensure that a product can only be assigned to restaurants owned by the same user.
        """
        user_restaurants = Restaurant.objects.filter(user=self.request.user)
        selected_restaurants = serializer.validated_data.get("restaurants")

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
    queryset = OrderProduct.objects.all()
    permission_classes = [IsAuthenticated]

    @staticmethod
    def has_permission(request, view):
        """Custom permission to allow only admins or restaurant owners to access the list."""
        return request.user.is_superuser or Restaurant.objects.filter(user=request.user).exists()

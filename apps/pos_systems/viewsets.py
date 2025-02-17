from rest_framework import viewsets, pagination
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from ..restaurants.models import Restaurant


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

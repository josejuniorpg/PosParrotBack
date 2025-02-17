from rest_framework import viewsets, pagination
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer
from ..restaurants.models import Restaurant


class CustomerPagination(pagination.PageNumberPagination):
    """
    Custom pagination for Customers.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class CustomerViewSet(viewsets.ModelViewSet, pagination.PageNumberPagination, IsAuthenticated):
    """
    API endpoint for managing customers.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomerPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Customer.objects.all()
        return Customer.objects.filter(restaurant__user=self.request.user)

    def has_permission(self, request, view):
        """Custom permission to allow only admins or restaurant owners to access the list."""
        return request.user.is_superuser or Restaurant.objects.filter(user=request.user).exists()

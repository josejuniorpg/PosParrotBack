from rest_framework import pagination, viewsets
from ..restaurants.models import Restaurant
from .models import Customer
from .serializers import CustomerSerializer


class CustomerPagination(pagination.PageNumberPagination):
    """
    Custom pagination for Customers.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class CustomerViewSet(viewsets.ModelViewSet, pagination.PageNumberPagination):
    """
    API endpoint for managing customers.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    pagination_class = CustomerPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Customer.objects.all()
        return Customer.objects.filter(restaurant__user=self.request.user)

    @staticmethod
    def has_permission(request, view):
        """Custom permission to allow only admins or restaurant owners to access the list."""
        return request.user.is_superuser or Restaurant.objects.filter(user=request.user).exists()

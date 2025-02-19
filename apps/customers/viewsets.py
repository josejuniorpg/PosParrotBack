from django.db import IntegrityError
from rest_framework import viewsets, serializers, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..restaurants.models import Restaurant
from .models import Customer
from .serializers import CustomerSerializer
from ..restaurants.permissions import IsRestaurantOwner


class CustomerPagination(PageNumberPagination):
    """
    Pagination for Customers.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing customers.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    pagination_class = CustomerPagination
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        """
        Filter customers based on the restaurant.
        """
        if self.request.user.is_superuser:
            return Customer.objects.all()

        restaurant_id = self.request.query_params.get("restaurant")

        # Verify the user is the owner of the restaurant
        if restaurant_id:
            if not Restaurant.objects.filter(id=restaurant_id, user=self.request.user).exists():
                raise PermissionDenied("You are not the owner of this restaurant.")
            return Customer.objects.filter(restaurant_id=restaurant_id)

        # If a restaurant is not specified, return customers from the user's restaurant
        return Customer.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        """
        Assign the customer to a specific restaurant based on the request parameters,
        ensuring the user owns the restaurant and avoiding duplicate emails.
        """
        restaurant_id = self.request.data.get("restaurant")

        if not restaurant_id:
            raise ValidationError("A restaurant ID is required in the query parameters.")

        # Ensure the user owns the specified restaurant
        if not Restaurant.objects.filter(id=restaurant_id, user=self.request.user).exists():
            raise ValidationError("You do not have permission to add customers to this restaurant.")

        restaurant = Restaurant.objects.get(id=restaurant_id)

        try:
            serializer.save(restaurant=restaurant)
        except IntegrityError:
            return Response({"error": "A customer with this email already exists in this restaurant."},
                            status=status.HTTP_400_BAD_REQUEST)

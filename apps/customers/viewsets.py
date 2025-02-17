from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing customers.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]

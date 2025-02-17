from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

# Create your views here.

class PublicTokenObtainPairView(TokenObtainPairView):
    """ Public view for obtaining a JWT token pair. """
    permission_classes = [AllowAny]


class PublicTokenRefreshView(TokenRefreshView):
    """ Public view for refreshing a JWT token. """
    permission_classes = [AllowAny]


class PublicTokenVerifyView(TokenVerifyView):
    """ Public view for verifying a JWT token. """
    permission_classes = [AllowAny]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import RestaurantViewSet, EmployeeViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
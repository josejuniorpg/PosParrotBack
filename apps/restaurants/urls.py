from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import EmployeeViewSet, RestaurantViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
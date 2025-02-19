from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VerifyEmployeeEmailView
from .viewsets import EmployeeViewSet, RestaurantViewSet, TableViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'tables', TableViewSet, basename='table')

urlpatterns = [
    path('', include(router.urls)),
    # Views Apis
    path('verify-employee-email/', VerifyEmployeeEmailView.as_view(), name='verify-employee-email'),
]

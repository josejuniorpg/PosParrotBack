from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DailyReportProductsView
from .viewsets import OrderViewSet, CategoryViewSet, ProductViewSet, OrderProductViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'order-products', OrderProductViewSet, basename='order-product')

urlpatterns = [
    path('', include(router.urls)),
    # View Apis
    path('daily-report/products/', DailyReportProductsView.as_view(), name='daily-report'),
]

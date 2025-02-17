from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.users.views import PublicTokenObtainPairView, PublicTokenRefreshView, PublicTokenVerifyView

schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant API",
        default_version="v1",
        description="API documentation for the restaurant management system",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', PublicTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', PublicTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', PublicTokenVerifyView.as_view(), name='token_verify'),

    path('api/', include('apps.restaurants.urls')),

    # 🔹 Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # 🔹 Redoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # 🔹 JSON OpenAPI Schema
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),

]

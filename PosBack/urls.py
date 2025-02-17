from django.contrib import admin
from django.urls import path, include

from apps.users.views import PublicTokenObtainPairView, PublicTokenRefreshView, PublicTokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', PublicTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', PublicTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', PublicTokenVerifyView.as_view(), name='token_verify'),

    path('api/', include('apps.restaurants.urls')),

]

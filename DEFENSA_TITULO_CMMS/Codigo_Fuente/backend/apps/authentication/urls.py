"""
Authentication URLs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    logout_view,
    current_user_view,
    change_password_view,
    verify_token_view,
    UserViewSet,
    UserManagementViewSet,
)

app_name = 'authentication'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user-management', UserManagementViewSet, basename='user-management')

urlpatterns = [
    # JWT Token endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='logout'),
    path('verify/', verify_token_view, name='verify_token'),
    
    # User endpoints
    path('me/', current_user_view, name='current_user'),
    path('change-password/', change_password_view, name='change_password'),
    
    # Router URLs
    path('', include(router.urls)),
]

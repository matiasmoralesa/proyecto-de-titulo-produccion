"""
Tests for authentication app.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Role

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Tests for User model."""
    
    def test_create_user(self, create_roles):
        """Test creating a user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=create_roles['operador']
        )
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
        assert user.role.name == Role.OPERADOR
        assert user.must_change_password is True
    
    def test_create_superuser(self, db):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.must_change_password is False
        assert user.role.name == Role.ADMIN
    
    def test_user_role_methods(self, admin_user, supervisor_user, operador_user):
        """Test user role checking methods."""
        assert admin_user.is_admin() is True
        assert admin_user.is_supervisor() is False
        assert admin_user.is_operador() is False
        
        assert supervisor_user.is_admin() is False
        assert supervisor_user.is_supervisor() is True
        assert supervisor_user.is_operador() is False
        
        assert operador_user.is_admin() is False
        assert operador_user.is_supervisor() is False
        assert operador_user.is_operador() is True


@pytest.mark.django_db
class TestAuthenticationEndpoints:
    """Tests for authentication endpoints."""
    
    def test_login_success(self, api_client, admin_user):
        """Test successful login."""
        url = reverse('authentication:token_obtain_pair')
        data = {
            'username': 'admin',
            'password': 'testpass123'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data
        assert response.data['user']['username'] == 'admin'
        assert response.data['user']['role'] == Role.ADMIN
    
    def test_login_invalid_credentials(self, api_client, admin_user):
        """Test login with invalid credentials."""
        url = reverse('authentication:token_obtain_pair')
        data = {
            'username': 'admin',
            'password': 'wrongpassword'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user(self, authenticated_client, admin_user):
        """Test getting current user data."""
        url = reverse('authentication:current_user')
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == admin_user.username
        assert response.data['email'] == admin_user.email
    
    def test_change_password(self, authenticated_client, admin_user):
        """Test changing password."""
        url = reverse('authentication:change_password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify password was changed
        admin_user.refresh_from_db()
        assert admin_user.check_password('newpass123')
        assert admin_user.must_change_password is False
    
    def test_change_password_wrong_old_password(self, authenticated_client):
        """Test changing password with wrong old password."""
        url = reverse('authentication:change_password')
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_change_password_mismatch(self, authenticated_client):
        """Test changing password with mismatched new passwords."""
        url = reverse('authentication:change_password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'differentpass123'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPermissions:
    """Tests for permission classes."""
    
    def test_admin_permission(self, api_client, admin_user, supervisor_user, operador_user):
        """Test IsAdmin permission."""
        from apps.authentication.permissions import IsAdmin
        from rest_framework.test import APIRequestFactory
        from rest_framework.views import APIView
        
        factory = APIRequestFactory()
        request = factory.get('/')
        permission = IsAdmin()
        
        # Admin should have permission
        request.user = admin_user
        assert permission.has_permission(request, APIView()) is True
        
        # Supervisor should not have permission
        request.user = supervisor_user
        assert permission.has_permission(request, APIView()) is False
        
        # Operador should not have permission
        request.user = operador_user
        assert permission.has_permission(request, APIView()) is False
    
    def test_supervisor_or_admin_permission(self, api_client, admin_user, supervisor_user, operador_user):
        """Test IsSupervisorOrAdmin permission."""
        from apps.authentication.permissions import IsSupervisorOrAdmin
        from rest_framework.test import APIRequestFactory
        from rest_framework.views import APIView
        
        factory = APIRequestFactory()
        request = factory.get('/')
        permission = IsSupervisorOrAdmin()
        
        # Admin should have permission
        request.user = admin_user
        assert permission.has_permission(request, APIView()) is True
        
        # Supervisor should have permission
        request.user = supervisor_user
        assert permission.has_permission(request, APIView()) is True
        
        # Operador should not have permission
        request.user = operador_user
        assert permission.has_permission(request, APIView()) is False


@pytest.mark.property
@pytest.mark.django_db
class TestTokenExpiration:
    """Property-based test for JWT token expiration."""
    
    def test_expired_token_returns_401(self, api_client, admin_user):
        """
        **Feature: cmms-local, Property 10: JWT Token Expiration**
        
        For any authenticated request, if the JWT token is expired,
        the Backend_API must return HTTP 401 Unauthorized.
        
        **Validates: Requirements 6.1**
        """
        from rest_framework_simplejwt.tokens import AccessToken
        from datetime import timedelta
        from django.utils import timezone
        
        # Create an expired token
        token = AccessToken.for_user(admin_user)
        token.set_exp(lifetime=timedelta(seconds=-1))  # Expired 1 second ago
        
        # Try to access protected endpoint with expired token
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
        url = reverse('authentication:current_user')
        response = api_client.get(url)
        
        # Should return 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

"""
Unit tests for user management functionality.
Tests Requirements: 10.2, 10.6
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.authentication.models import Role

User = get_user_model()


@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()


@pytest.fixture
def admin_role(db):
    """Create admin role."""
    return Role.objects.get_or_create(
        name=Role.ADMIN,
        defaults={'description': 'Administrator'}
    )[0]


@pytest.fixture
def supervisor_role(db):
    """Create supervisor role."""
    return Role.objects.get_or_create(
        name=Role.SUPERVISOR,
        defaults={'description': 'Supervisor'}
    )[0]


@pytest.fixture
def operador_role(db):
    """Create operador role."""
    return Role.objects.get_or_create(
        name=Role.OPERADOR,
        defaults={'description': 'Operador'}
    )[0]


@pytest.fixture
def admin_user(db, admin_role):
    """Create admin user."""
    return User.objects.create_user(
        username='admin_test',
        email='admin@test.com',
        password='admin123',
        role=admin_role,
        must_change_password=False
    )


@pytest.fixture
def supervisor_user(db, supervisor_role):
    """Create supervisor user."""
    return User.objects.create_user(
        username='supervisor_test',
        email='supervisor@test.com',
        password='supervisor123',
        role=supervisor_role,
        must_change_password=False
    )


@pytest.fixture
def operador_user(db, operador_role):
    """Create operador user."""
    return User.objects.create_user(
        username='operador_test',
        email='operador@test.com',
        password='operador123',
        role=operador_role,
        must_change_password=False
    )


@pytest.mark.django_db
class TestUserManagementPermissions:
    """Test user management permissions (ADMIN only)."""
    
    def test_admin_can_list_users(self, api_client, admin_user):
        """Test that admin can list users."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/v1/auth/user-management/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_supervisor_cannot_list_users(self, api_client, supervisor_user):
        """Test that supervisor cannot list users."""
        api_client.force_authenticate(user=supervisor_user)
        response = api_client.get('/api/v1/auth/user-management/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_operador_cannot_list_users(self, api_client, operador_user):
        """Test that operador cannot list users."""
        api_client.force_authenticate(user=operador_user)
        response = api_client.get('/api/v1/auth/user-management/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_unauthenticated_cannot_list_users(self, api_client):
        """Test that unauthenticated users cannot list users."""
        response = api_client.get('/api/v1/auth/user-management/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserCreation:
    """Test user creation functionality."""
    
    def test_admin_can_create_user(self, api_client, admin_user, operador_role):
        """Test that admin can create a new user."""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'NewPass123!',
            'password_confirm': 'NewPass123!',
            'first_name': 'New',
            'last_name': 'User',
            'role': operador_role.id
        }
        
        response = api_client.post('/api/v1/auth/user-management/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'newuser'
        assert response.data['email'] == 'newuser@test.com'
        assert response.data['must_change_password'] is True
    
    def test_create_user_with_duplicate_username(self, api_client, admin_user, operador_user, operador_role):
        """Test that creating user with duplicate username fails."""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'username': operador_user.username,  # Duplicate
            'email': 'different@test.com',
            'password': 'NewPass123!',
            'password_confirm': 'NewPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': operador_role.id
        }
        
        response = api_client.post('/api/v1/auth/user-management/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_user_with_duplicate_email(self, api_client, admin_user, operador_user, operador_role):
        """Test that creating user with duplicate email fails."""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'username': 'newuser',
            'email': operador_user.email,  # Duplicate
            'password': 'NewPass123!',
            'password_confirm': 'NewPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': operador_role.id
        }
        
        response = api_client.post('/api/v1/auth/user-management/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_user_with_mismatched_passwords(self, api_client, admin_user, operador_role):
        """Test that creating user with mismatched passwords fails."""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'NewPass123!',
            'password_confirm': 'DifferentPass123!',  # Mismatch
            'first_name': 'Test',
            'last_name': 'User',
            'role': operador_role.id
        }
        
        response = api_client.post('/api/v1/auth/user-management/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserUpdate:
    """Test user update functionality."""
    
    def test_admin_can_update_user(self, api_client, admin_user, operador_user):
        """Test that admin can update user information."""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '123-456-7890'
        }
        
        response = api_client.patch(f'/api/v1/auth/user-management/{operador_user.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Name'
        assert response.data['phone'] == '123-456-7890'
    
    def test_cannot_update_password_through_update_endpoint(self, api_client, admin_user, operador_user):
        """Test that password cannot be updated through update endpoint."""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'password': 'NewPassword123!'
        }
        
        response = api_client.patch(f'/api/v1/auth/user-management/{operador_user.id}/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserActivationDeactivation:
    """Test user activation and deactivation."""
    
    def test_admin_can_deactivate_user(self, api_client, admin_user, operador_user):
        """Test that admin can deactivate a user."""
        api_client.force_authenticate(user=admin_user)
        
        response = api_client.post(f'/api/v1/auth/user-management/{operador_user.id}/deactivate/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_active'] is False
    
    def test_admin_can_activate_user(self, api_client, admin_user, operador_user):
        """Test that admin can activate a user."""
        api_client.force_authenticate(user=admin_user)
        
        # First deactivate
        operador_user.is_active = False
        operador_user.save()
        
        # Then activate
        response = api_client.post(f'/api/v1/auth/user-management/{operador_user.id}/activate/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_active'] is True
    
    def test_admin_cannot_deactivate_self(self, api_client, admin_user):
        """Test that admin cannot deactivate their own account."""
        api_client.force_authenticate(user=admin_user)
        
        response = api_client.post(f'/api/v1/auth/user-management/{admin_user.id}/deactivate/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_soft_delete_deactivates_user(self, api_client, admin_user, operador_user):
        """Test that deleting a user deactivates them (soft delete)."""
        api_client.force_authenticate(user=admin_user)
        
        response = api_client.delete(f'/api/v1/auth/user-management/{operador_user.id}/')
        assert response.status_code == status.HTTP_200_OK
        
        # Verify user is deactivated, not deleted
        operador_user.refresh_from_db()
        assert operador_user.is_active is False


@pytest.mark.django_db
class TestPasswordReset:
    """Test password reset functionality."""
    
    def test_admin_can_reset_user_password(self, api_client, admin_user, operador_user):
        """Test that admin can reset user password."""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'new_password': 'ResetPass123!',
            'new_password_confirm': 'ResetPass123!'
        }
        
        response = api_client.post(f'/api/v1/auth/user-management/{operador_user.id}/reset_password/', data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify user must change password
        operador_user.refresh_from_db()
        assert operador_user.must_change_password is True
        
        # Verify password was changed
        assert operador_user.check_password('ResetPass123!')
    
    def test_reset_password_with_mismatched_passwords(self, api_client, admin_user, operador_user):
        """Test that resetting password with mismatched passwords fails."""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'new_password': 'ResetPass123!',
            'new_password_confirm': 'DifferentPass123!'
        }
        
        response = api_client.post(f'/api/v1/auth/user-management/{operador_user.id}/reset_password/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPasswordHashing:
    """Test password hashing (Requirement 10.6)."""
    
    def test_password_is_hashed_on_creation(self, db, operador_role):
        """Test that password is hashed when creating a user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='TestPass123!',
            role=operador_role
        )
        
        # Password should not be stored in plain text
        assert user.password != 'TestPass123!'
        # Password should be hashed
        assert user.password.startswith('pbkdf2_sha256$')
        # check_password should work
        assert user.check_password('TestPass123!')
    
    def test_password_is_hashed_on_update(self, db, operador_user):
        """Test that password is hashed when updating a user."""
        operador_user.set_password('NewPass123!')
        operador_user.save()
        
        # Password should not be stored in plain text
        assert operador_user.password != 'NewPass123!'
        # Password should be hashed
        assert operador_user.password.startswith('pbkdf2_sha256$')
        # check_password should work
        assert operador_user.check_password('NewPass123!')


@pytest.mark.django_db
class TestUserFiltering:
    """Test user filtering functionality."""
    
    def test_filter_users_by_role(self, api_client, admin_user, supervisor_user, operador_user):
        """Test filtering users by role."""
        api_client.force_authenticate(user=admin_user)
        
        response = api_client.get('/api/v1/auth/user-management/?role=OPERADOR')
        assert response.status_code == status.HTTP_200_OK
        
        # Should only return operador users
        results = response.data.get('results', response.data)
        for user in results:
            assert user['role_name'] == 'OPERADOR'
    
    def test_filter_users_by_active_status(self, api_client, admin_user, operador_user):
        """Test filtering users by active status."""
        api_client.force_authenticate(user=admin_user)
        
        # Deactivate operador user
        operador_user.is_active = False
        operador_user.save()
        
        # Filter for active users
        response = api_client.get('/api/v1/auth/user-management/?is_active=true')
        assert response.status_code == status.HTTP_200_OK
        
        results = response.data.get('results', response.data)
        for user in results:
            assert user['is_active'] is True
    
    def test_search_users(self, api_client, admin_user, operador_user):
        """Test searching users by username, email, or name."""
        api_client.force_authenticate(user=admin_user)
        
        # Update operador user for testing
        operador_user.first_name = 'SearchTest'
        operador_user.save()
        
        response = api_client.get('/api/v1/auth/user-management/?search=SearchTest')
        assert response.status_code == status.HTTP_200_OK
        
        results = response.data.get('results', response.data)
        assert len(results) > 0
        assert any(user['first_name'] == 'SearchTest' for user in results)

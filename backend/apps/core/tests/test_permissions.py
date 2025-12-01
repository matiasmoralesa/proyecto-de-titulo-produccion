"""
Unit tests for permission classes
Tests each permission class with different roles and edge cases.
"""
import pytest
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from apps.core.permissions import (
    IsAdminOnly,
    IsSupervisorOrAbove,
    IsOperadorOrAbove,
    IsOwnerOrSupervisor,
    IsOwnerOrAdmin,
    ReadOnlyForOperador,
)
from apps.authentication.models import Role

User = get_user_model()


@pytest.fixture
def api_factory():
    """Create API request factory"""
    return APIRequestFactory()


@pytest.fixture
@pytest.mark.django_db
def users(roles):
    """Create test users with different roles"""
    admin = User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='testpass123',
        role=roles['admin']
    )
    
    supervisor = User.objects.create_user(
        username='supervisor',
        email='supervisor@test.com',
        password='testpass123',
        role=roles['supervisor']
    )
    
    operator = User.objects.create_user(
        username='operator',
        email='operator@test.com',
        password='testpass123',
        role=roles['operator']
    )
    
    return {'admin': admin, 'supervisor': supervisor, 'operator': operator}


@pytest.mark.django_db
class TestIsAdminOnly:
    """Test IsAdminOnly permission class"""
    
    def test_admin_has_permission(self, api_factory, users):
        """Test that admin users have permission"""
        request = api_factory.get('/')
        request.user = users['admin']
        
        permission = IsAdminOnly()
        assert permission.has_permission(request, None) is True
    
    def test_supervisor_denied(self, api_factory, users):
        """Test that supervisor users are denied"""
        request = api_factory.get('/')
        request.user = users['supervisor']
        
        permission = IsAdminOnly()
        assert permission.has_permission(request, None) is False
    
    def test_operator_denied(self, api_factory, users):
        """Test that operator users are denied"""
        request = api_factory.get('/')
        request.user = users['operator']
        
        permission = IsAdminOnly()
        assert permission.has_permission(request, None) is False
    
    def test_unauthenticated_denied(self, api_factory):
        """Test that unauthenticated users are denied"""
        request = api_factory.get('/')
        request.user = None
        
        permission = IsAdminOnly()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsSupervisorOrAbove:
    """Test IsSupervisorOrAbove permission class"""
    
    def test_admin_has_permission(self, api_factory, users):
        """Test that admin users have permission"""
        request = api_factory.get('/')
        request.user = users['admin']
        
        permission = IsSupervisorOrAbove()
        assert permission.has_permission(request, None) is True
    
    def test_supervisor_has_permission(self, api_factory, users):
        """Test that supervisor users have permission"""
        request = api_factory.get('/')
        request.user = users['supervisor']
        
        permission = IsSupervisorOrAbove()
        assert permission.has_permission(request, None) is True
    
    def test_operator_denied(self, api_factory, users):
        """Test that operator users are denied"""
        request = api_factory.get('/')
        request.user = users['operator']
        
        permission = IsSupervisorOrAbove()
        assert permission.has_permission(request, None) is False
    
    def test_unauthenticated_denied(self, api_factory):
        """Test that unauthenticated users are denied"""
        request = api_factory.get('/')
        request.user = None
        
        permission = IsSupervisorOrAbove()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsOperadorOrAbove:
    """Test IsOperadorOrAbove permission class"""
    
    def test_admin_has_permission(self, api_factory, users):
        """Test that admin users have permission"""
        request = api_factory.get('/')
        request.user = users['admin']
        
        permission = IsOperadorOrAbove()
        assert permission.has_permission(request, None) is True
    
    def test_supervisor_has_permission(self, api_factory, users):
        """Test that supervisor users have permission"""
        request = api_factory.get('/')
        request.user = users['supervisor']
        
        permission = IsOperadorOrAbove()
        assert permission.has_permission(request, None) is True
    
    def test_operator_has_permission(self, api_factory, users):
        """Test that operator users have permission"""
        request = api_factory.get('/')
        request.user = users['operator']
        
        permission = IsOperadorOrAbove()
        assert permission.has_permission(request, None) is True
    
    def test_unauthenticated_denied(self, api_factory):
        """Test that unauthenticated users are denied"""
        request = api_factory.get('/')
        request.user = None
        
        permission = IsOperadorOrAbove()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsOwnerOrSupervisor:
    """Test IsOwnerOrSupervisor permission class"""
    
    @pytest.fixture
    def mock_object(self, users):
        """Create a mock object with ownership"""
        class MockObject:
            def __init__(self, assigned_to=None):
                self.id = 1
                self.assigned_to = assigned_to
        
        return MockObject
    
    def test_admin_has_object_permission(self, api_factory, users, mock_object):
        """Test that admin users have permission on any object"""
        request = api_factory.get('/')
        request.user = users['admin']
        
        obj = mock_object(assigned_to=users['operator'])
        
        permission = IsOwnerOrSupervisor()
        assert permission.has_object_permission(request, None, obj) is True
    
    def test_supervisor_has_object_permission(self, api_factory, users, mock_object):
        """Test that supervisor users have permission on any object"""
        request = api_factory.get('/')
        request.user = users['supervisor']
        
        obj = mock_object(assigned_to=users['operator'])
        
        permission = IsOwnerOrSupervisor()
        assert permission.has_object_permission(request, None, obj) is True
    
    def test_owner_has_object_permission(self, api_factory, users, mock_object):
        """Test that owner has permission on their own object"""
        request = api_factory.get('/')
        request.user = users['operator']
        
        obj = mock_object(assigned_to=users['operator'])
        
        permission = IsOwnerOrSupervisor()
        assert permission.has_object_permission(request, None, obj) is True
    
    def test_non_owner_operator_denied(self, api_factory, users, mock_object):
        """Test that non-owner operator is denied"""
        request = api_factory.get('/')
        request.user = users['operator']
        
        # Create another operator
        other_operator = User.objects.create_user(
            username='other_operator',
            email='other@test.com',
            password='testpass123',
            role=users['operator'].role
        )
        
        obj = mock_object(assigned_to=other_operator)
        
        permission = IsOwnerOrSupervisor()
        assert permission.has_object_permission(request, None, obj) is False
    
    def test_unauthenticated_denied_permission(self, api_factory):
        """Test that unauthenticated users are denied at permission level"""
        from django.contrib.auth.models import AnonymousUser
        
        request = api_factory.get('/')
        request.user = AnonymousUser()
        
        permission = IsOwnerOrSupervisor()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsOwnerOrAdmin:
    """Test IsOwnerOrAdmin permission class"""
    
    @pytest.fixture
    def mock_object(self, users):
        """Create a mock object with ownership"""
        class MockObject:
            def __init__(self, user=None):
                self.id = 1
                self.user = user
        
        return MockObject
    
    def test_admin_has_object_permission(self, api_factory, users, mock_object):
        """Test that admin users have permission on any object"""
        request = api_factory.get('/')
        request.user = users['admin']
        
        obj = mock_object(user=users['operator'])
        
        permission = IsOwnerOrAdmin()
        assert permission.has_object_permission(request, None, obj) is True
    
    def test_supervisor_denied_on_others_object(self, api_factory, users, mock_object):
        """Test that supervisor is denied on objects they don't own"""
        request = api_factory.get('/')
        request.user = users['supervisor']
        
        obj = mock_object(user=users['operator'])
        
        permission = IsOwnerOrAdmin()
        assert permission.has_object_permission(request, None, obj) is False
    
    def test_owner_has_object_permission(self, api_factory, users, mock_object):
        """Test that owner has permission on their own object"""
        request = api_factory.get('/')
        request.user = users['operator']
        
        obj = mock_object(user=users['operator'])
        
        permission = IsOwnerOrAdmin()
        assert permission.has_object_permission(request, None, obj) is True


@pytest.mark.django_db
class TestReadOnlyForOperador:
    """Test ReadOnlyForOperador permission class"""
    
    def test_admin_has_write_permission(self, api_factory, users):
        """Test that admin users have write permission"""
        request = api_factory.post('/')
        request.user = users['admin']
        
        permission = ReadOnlyForOperador()
        assert permission.has_permission(request, None) is True
    
    def test_supervisor_has_write_permission(self, api_factory, users):
        """Test that supervisor users have write permission"""
        request = api_factory.post('/')
        request.user = users['supervisor']
        
        permission = ReadOnlyForOperador()
        assert permission.has_permission(request, None) is True
    
    def test_operator_has_read_permission(self, api_factory, users):
        """Test that operator users have read permission"""
        request = api_factory.get('/')
        request.user = users['operator']
        
        permission = ReadOnlyForOperador()
        assert permission.has_permission(request, None) is True
    
    def test_operator_denied_write_permission(self, api_factory, users):
        """Test that operator users are denied write permission"""
        request = api_factory.post('/')
        request.user = users['operator']
        
        permission = ReadOnlyForOperador()
        assert permission.has_permission(request, None) is False
    
    def test_operator_denied_put_permission(self, api_factory, users):
        """Test that operator users are denied PUT permission"""
        request = api_factory.put('/')
        request.user = users['operator']
        
        permission = ReadOnlyForOperador()
        assert permission.has_permission(request, None) is False
    
    def test_operator_denied_delete_permission(self, api_factory, users):
        """Test that operator users are denied DELETE permission"""
        request = api_factory.delete('/')
        request.user = users['operator']
        
        permission = ReadOnlyForOperador()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestEdgeCases:
    """Test edge cases for permission classes"""
    
    def test_user_without_role_denied(self, api_factory, roles):
        """Test that user without role is denied"""
        # Create user with a default role (since role is required)
        # Then test with invalid role name
        invalid_role = Role.objects.create(
            name='GUEST',
            description='Guest role without permissions'
        )
        
        user = User.objects.create_user(
            username='norole',
            email='norole@test.com',
            password='testpass123',
            role=invalid_role
        )
        
        request = api_factory.get('/')
        request.user = user
        
        # Should be denied because role is not in valid roles
        permission = IsOperadorOrAbove()
        assert permission.has_permission(request, None) is False
    
    def test_invalid_role_name_denied(self, api_factory):
        """Test that user with invalid role name is denied"""
        # Create role with invalid name
        invalid_role = Role.objects.create(
            name='INVALID_ROLE',
            description='Invalid role'
        )
        
        user = User.objects.create_user(
            username='invalidrole',
            email='invalid@test.com',
            password='testpass123',
            role=invalid_role
        )
        
        request = api_factory.get('/')
        request.user = user
        
        permission = IsOperadorOrAbove()
        assert permission.has_permission(request, None) is False

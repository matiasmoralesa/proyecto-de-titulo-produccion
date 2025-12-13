"""
Pytest fixtures for security tests
"""
import pytest
from django.contrib.auth import get_user_model
from apps.authentication.models import Role

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def roles():
    """Create test roles"""
    admin_role, _ = Role.objects.get_or_create(
        name='ADMIN',
        defaults={'description': 'Administrator'}
    )
    supervisor_role, _ = Role.objects.get_or_create(
        name='SUPERVISOR',
        defaults={'description': 'Supervisor'}
    )
    operator_role, _ = Role.objects.get_or_create(
        name='OPERADOR',
        defaults={'description': 'Operator'}
    )
    return {
        'admin': admin_role,
        'supervisor': supervisor_role,
        'operator': operator_role
    }


@pytest.fixture
@pytest.mark.django_db
def test_user(roles):
    """Create a test user with operator role"""
    user = User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='testpass123'
    )
    user.role = roles['operator']
    user.save()
    return user

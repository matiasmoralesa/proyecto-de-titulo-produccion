"""
Pytest configuration and fixtures.
"""
import pytest
from django.contrib.auth import get_user_model
from apps.authentication.models import Role

User = get_user_model()


@pytest.fixture
def api_client():
    """Return API client for testing."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_roles(db):
    """Create all roles."""
    roles = {}
    for role_name, role_display in Role.ROLE_CHOICES:
        role, _ = Role.objects.get_or_create(
            name=role_name,
            defaults={'description': f'{role_display} role'}
        )
        roles[role_name.lower()] = role
    return roles


@pytest.fixture
def admin_user(db, create_roles):
    """Create admin user."""
    user = User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='testpass123',
        role=create_roles['admin'],
        must_change_password=False
    )
    return user


@pytest.fixture
def supervisor_user(db, create_roles):
    """Create supervisor user."""
    user = User.objects.create_user(
        username='supervisor',
        email='supervisor@test.com',
        password='testpass123',
        role=create_roles['supervisor'],
        must_change_password=False
    )
    return user


@pytest.fixture
def operador_user(db, create_roles):
    """Create operador user."""
    user = User.objects.create_user(
        username='operador',
        email='operador@test.com',
        password='testpass123',
        role=create_roles['operador'],
        must_change_password=False
    )
    return user


@pytest.fixture
def authenticated_client(api_client, admin_user):
    """Return authenticated API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client

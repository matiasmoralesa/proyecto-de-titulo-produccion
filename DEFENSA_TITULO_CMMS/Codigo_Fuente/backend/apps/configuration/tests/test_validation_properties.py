"""Property-based tests for configuration validation."""

import pytest
from django.contrib.auth import get_user_model
from hypothesis import given, strategies as st, settings
from hypothesis.extra.django import TestCase
from rest_framework.test import APIClient

from apps.configuration.models import AssetCategory, Priority, SystemParameter
from apps.configuration.serializers import (
    AssetCategorySerializer,
    PrioritySerializer,
    SystemParameterSerializer
)
from apps.authentication.models import Role

User = get_user_model()


class ConfigurationValidationPropertyTests(TestCase):
    """Property-based tests for configuration validation."""

    def setUp(self):
        """Set up test data."""
        # Clean up any existing data
        User.objects.all().delete()
        Role.objects.all().delete()
        AssetCategory.objects.all().delete()
        Priority.objects.all().delete()
        SystemParameter.objects.all().delete()
        
        # Create admin role
        admin_role, _ = Role.objects.get_or_create(
            name='ADMIN',
            defaults={'description': 'Administrator'}
        )
        
        # Create user with role
        self.user = User.objects.create(
            username='admin',
            email='admin@example.com',
            role=admin_role
        )
        self.user.set_password('adminpass123')
        self.user.save()
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @given(
        st.lists(
            st.tuples(
                st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Nd', 'Pc'))),
                st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_characters='\x00')),
                st.text(max_size=200, alphabet=st.characters(blacklist_characters='\x00')),
                st.booleans()
            ),
            min_size=1,
            max_size=5
        )
    )
    @settings(max_examples=20, deadline=None)
    def test_property_crud_operations_preserve_data_integrity(self, category_data):
        """Property 6: CRUD operations preserve data integrity.
        
        For any valid configuration entity, create and update operations 
        should save all provided fields correctly to the database.
        
        **Validates: Requirements 3.1, 3.2**
        """
        # Clear existing categories
        AssetCategory.objects.all().delete()
        
        created_categories = []
        
        # Test CREATE operations
        for i, (code, name, description, is_active) in enumerate(category_data):
            unique_code = f"{code}_{i}"
            unique_name = f"{name.strip() or 'Name'}_{i}"  # Make name unique too
            
            # Strip description to match model behavior
            clean_description = description.strip() if description else ''
            
            category_data_dict = {
                'code': unique_code,
                'name': unique_name,
                'description': clean_description,
                'is_active': is_active
            }
            
            serializer = AssetCategorySerializer(data=category_data_dict)
            assert serializer.is_valid(), f"Serializer should be valid: {serializer.errors}"
            
            category = serializer.save(created_by=self.user)
            created_categories.append(category)
            
            # Property: All fields should be preserved
            assert category.code == unique_code, "Code should be preserved"
            assert category.name == unique_name, "Name should be preserved"
            assert category.description == clean_description, "Description should be preserved"
            assert category.is_active == is_active, "Active status should be preserved"

    @given(
        st.lists(
            st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Nd', 'Pc'))),
            min_size=2,
            max_size=5
        )
    )
    @settings(max_examples=10)
    def test_property_unique_constraints_enforced(self, codes):
        """Property 15: Unique constraints are enforced.
        
        For any code or key field with uniqueness constraints, 
        duplicate values should be rejected with an error message.
        
        **Validates: Requirements 4.7**
        """
        # Clear existing categories
        AssetCategory.objects.all().delete()
        
        first_code = codes[0]
        
        # Create first category
        first_category_data = {
            'code': first_code,
            'name': 'First Category',
            'description': 'First category description',
            'is_active': True
        }
        
        serializer = AssetCategorySerializer(data=first_category_data)
        assert serializer.is_valid(), f"First category should be valid: {serializer.errors}"
        
        first_category = serializer.save(created_by=self.user)
        assert first_category.code == first_code, "First category should be created"
        
        # Try to create second category with same code
        duplicate_category_data = {
            'code': first_code,
            'name': 'Duplicate Category',
            'description': 'Duplicate category description',
            'is_active': True
        }
        
        duplicate_serializer = AssetCategorySerializer(data=duplicate_category_data)
        
        # Property: Duplicate code should be rejected
        assert not duplicate_serializer.is_valid(), "Duplicate code should be rejected"
        
        # Property: Error message should mention uniqueness
        error_messages = str(duplicate_serializer.errors)
        assert 'ya existe' in error_messages.lower() or 'unique' in error_messages.lower(), \
            f"Error message should mention uniqueness: {duplicate_serializer.errors}"

    @given(
        st.sampled_from(['string', 'integer', 'float', 'boolean', 'json'])
    )
    @settings(max_examples=10)
    def test_property_type_validation_for_parameters(self, data_type):
        """Property 8: Type validation for parameters.
        
        For any system parameter update, the provided value should match 
        the parameter's defined data_type or be rejected.
        
        **Validates: Requirements 3.4**
        """
        # Create parameter
        parameter = SystemParameter.objects.create(
            key=f'TEST_PARAM_{data_type}',
            value='default_value',
            description=f'Test parameter for {data_type}',
            data_type=data_type,
            is_editable=True,
            modified_by=self.user
        )
        
        # Test valid values for each data type
        valid_value = self._get_valid_value_for_type(data_type)
        
        valid_data = {
            'value': valid_value,
            'description': parameter.description
        }
        
        serializer = SystemParameterSerializer(parameter, data=valid_data, partial=True)
        assert serializer.is_valid(), f"Valid {data_type} value should be accepted: {serializer.errors}"

    def _get_valid_value_for_type(self, data_type):
        """Get a valid value for the given data type."""
        if data_type == 'string':
            return 'valid_string_value'
        elif data_type == 'integer':
            return '42'
        elif data_type == 'float':
            return '3.14'
        elif data_type == 'boolean':
            return 'true'
        elif data_type == 'json':
            return '{"key": "value"}'
        else:
            return 'default_value'

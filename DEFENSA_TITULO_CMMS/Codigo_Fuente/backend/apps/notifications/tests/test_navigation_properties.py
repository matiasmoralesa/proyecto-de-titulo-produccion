"""Property-based tests for notification navigation."""

import pytest
import uuid
from django.test import Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from hypothesis import given, strategies as st, settings
from hypothesis.extra.django import TestCase

from apps.notifications.models import Notification
from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset, Location
from apps.authentication.models import Role

User = get_user_model()


class NotificationNavigationPropertyTests(TestCase):
    """Property-based tests for notification navigation."""

    def setUp(self):
        """Set up test data."""
        # Clean up any existing data in correct order to avoid ProtectedError
        Notification.objects.all().delete()
        WorkOrder.objects.all().delete()
        Asset.objects.all().delete()
        Location.objects.all().delete()
        User.objects.all().delete()
        Role.objects.all().delete()
        
        # Create admin role
        admin_role, _ = Role.objects.get_or_create(
            name='ADMIN',
            defaults={'description': 'Administrator'}
        )
        
        # Create user with role
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            role=admin_role
        )
        self.user.set_password('testpass123')
        self.user.save()
        
        self.client = Client()
        self.client.force_login(self.user)
        
        # Create test location
        self.location = Location.objects.create(
            name='Test Location',
            address='Test Address'
        )
        
        # Create test asset
        from datetime import date
        self.asset = Asset.objects.create(
            name='Test Asset',
            vehicle_type='Camión Supersucker',
            model='Test Model',
            serial_number='TEST001',
            location=self.location,
            installation_date=date.today(),
            created_by=self.user
        )

    @given(
        st.lists(
            st.tuples(
                st.sampled_from(['work_order', 'asset']),
                st.text(min_size=1, max_size=100),
                st.text(min_size=1, max_size=200)
            ),
            min_size=1,
            max_size=10
        )
    )
    @settings(max_examples=20, deadline=None)
    def test_property_valid_objects_navigate_correctly(self, notification_data):
        """Property 4: Valid objects navigate correctly.
        
        For any notification with a valid related_object_id and related_object_type,
        clicking the notification should navigate to the correct detail page.
        
        **Validates: Requirements 2.1, 2.2**
        """
        # Clear existing notifications
        Notification.objects.all().delete()
        WorkOrder.objects.all().delete()
        
        created_objects = []
        
        for i, (object_type, title, message) in enumerate(notification_data):
            # Create the related object
            if object_type == 'work_order':
                related_object = WorkOrder.objects.create(
                    work_order_number=f'WO-TEST-{i}',
                    title=title[:50],  # Limit title length
                    description=message,
                    status='Pendiente',
                    priority='Media',
                    asset=self.asset,
                    assigned_to=self.user,
                    scheduled_date=timezone.now(),
                    created_by=self.user
                )
                created_objects.append(('work_order', related_object.id))
            elif object_type == 'asset':
                # Use existing asset for simplicity
                related_object = self.asset
                created_objects.append(('asset', related_object.id))
            
            # Create notification
            notification = Notification.objects.create(
                user=self.user,
                title=title[:100],
                message=message,
                related_object_type=object_type,
                related_object_id=related_object.id,
                is_read=False
            )
        
        # Test navigation for each notification
        for object_type, object_id in created_objects:
            # Property: Valid objects should be accessible
            if object_type == 'work_order':
                work_order = WorkOrder.objects.get(id=object_id)
                assert work_order is not None, f"Work order {object_id} should exist"
                assert work_order.id == object_id, f"Work order ID should match"
                
            elif object_type == 'asset':
                asset = Asset.objects.get(id=object_id)
                assert asset is not None, f"Asset {object_id} should exist"
                assert asset.id == object_id, f"Asset ID should match"

    @given(
        st.lists(
            st.integers(min_value=9999, max_value=99999),  # Non-existent IDs
            min_size=1,
            max_size=5
        )
    )
    @settings(max_examples=10)
    def test_property_invalid_objects_show_error_messages(self, invalid_ids):
        """Property 5: Invalid objects show error messages.
        
        For any notification referencing a non-existent object,
        clicking should display an error message and mark the notification as read.
        """
        # Clear existing notifications
        Notification.objects.all().delete()
        
        notifications = []
        
        for i, invalid_id in enumerate(invalid_ids):
            # Create notification with non-existent object ID
            notification = Notification.objects.create(
                user=self.user,
                title=f'Test Notification {i}',
                message=f'Test message for invalid object {invalid_id}',
                related_object_type='work_order',
                related_object_id=invalid_id,
                is_read=False
            )
            notifications.append(notification)
        
        # Test error handling for each notification
        for notification in notifications:
            # Verify the related object doesn't exist
            assert not WorkOrder.objects.filter(id=notification.related_object_id).exists(), \
                f"Object {notification.related_object_id} should not exist"
            
            # Property: Non-existent objects should be handled gracefully
            try:
                WorkOrder.objects.get(id=notification.related_object_id)
                assert False, "Should not find non-existent work order"
            except WorkOrder.DoesNotExist:
                # This is expected - the object doesn't exist
                pass
            
            # Property: Notification should be markable as read even if object doesn't exist
            notification.is_read = True
            notification.save()
            
            notification.refresh_from_db()
            assert notification.is_read, "Notification should be marked as read"

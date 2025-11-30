"""
Unit tests for machine status functionality.
Tests Requirements: 11.2, 11.4
"""
import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from apps.authentication.models import Role, User
from apps.assets.models import Asset, Location
from apps.work_orders.models import WorkOrder
from apps.machine_status.models import AssetStatus, AssetStatusHistory


@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()


@pytest.fixture
def location(db):
    """Create a location."""
    return Location.objects.create(
        name='Test Location',
        address='Test Address'
    )


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


@pytest.fixture
def asset(db, location, admin_user):
    """Create an asset."""
    return Asset.objects.create(
        name='Test Asset',
        vehicle_type='CAMION_SUPERSUCKER',
        model='Test Model',
        serial_number='TEST123',
        location=location,
        installation_date=timezone.now().date(),
        status='ACTIVE',
        created_by=admin_user
    )


@pytest.fixture
def asset_status(db, asset, admin_user):
    """Create asset status."""
    return AssetStatus.objects.create(
        asset=asset,
        status_type=AssetStatus.OPERANDO,
        odometer_reading=1000.0,
        fuel_level=80,
        condition_notes='Good condition',
        last_updated_by=admin_user
    )


@pytest.mark.django_db
class TestAssetStatusPermissions:
    """Test asset status permissions."""
    
    def test_admin_can_view_all_statuses(self, api_client, admin_user, asset_status):
        """Test that admin can view all asset statuses."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/v1/machine-status/status/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_supervisor_can_view_all_statuses(self, api_client, supervisor_user, asset_status):
        """Test that supervisor can view all asset statuses."""
        api_client.force_authenticate(user=supervisor_user)
        response = api_client.get('/api/v1/machine-status/status/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_operador_can_only_view_assigned_assets(self, api_client, operador_user, asset, asset_status):
        """Test that operador can only view assigned asset statuses."""
        api_client.force_authenticate(user=operador_user)
        
        # Without assignment, should see no statuses
        response = api_client.get('/api/v1/machine-status/status/')
        assert response.status_code == status.HTTP_200_OK
        results = response.data.get('results', response.data)
        assert len(results) == 0
        
        # Create work order assignment
        WorkOrder.objects.create(
            work_order_number='WO-TEST-001',
            title='Test Work Order',
            description='Test',
            priority='MEDIUM',
            status='IN_PROGRESS',
            asset=asset,
            assigned_to=operador_user,
            scheduled_date=timezone.now(),
            created_by=operador_user
        )
        
        # Now should see the status
        response = api_client.get('/api/v1/machine-status/status/')
        assert response.status_code == status.HTTP_200_OK
        results = response.data.get('results', response.data)
        assert len(results) == 1


@pytest.mark.django_db
class TestAssetStatusUpdate:
    """Test asset status update functionality."""
    
    def test_admin_can_update_any_asset_status(self, api_client, admin_user, asset_status):
        """Test that admin can update any asset status."""
        api_client.force_authenticate(user=admin_user)
        
        data = {
            'status_type': AssetStatus.EN_MANTENIMIENTO,
            'odometer_reading': 1100.0,
            'fuel_level': 70,
            'condition_notes': 'Scheduled maintenance'
        }
        
        response = api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status_type'] == AssetStatus.EN_MANTENIMIENTO
    
    def test_operador_can_only_update_assigned_assets(self, api_client, operador_user, asset, asset_status):
        """Test that operador can only update assigned asset statuses."""
        api_client.force_authenticate(user=operador_user)
        
        data = {
            'status_type': AssetStatus.EN_MANTENIMIENTO,
        }
        
        # Without assignment, should not be able to see the status (404)
        response = api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Create work order assignment
        WorkOrder.objects.create(
            work_order_number='WO-TEST-002',
            title='Test Work Order',
            description='Test',
            priority='MEDIUM',
            status='IN_PROGRESS',
            asset=asset,
            assigned_to=operador_user,
            scheduled_date=timezone.now(),
            created_by=operador_user
        )
        
        # Now should succeed
        response = api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestStatusHistoryAuditTrail:
    """Test status history audit trail (Requirement 11.4)."""
    
    def test_status_update_creates_history_record(self, api_client, admin_user, asset_status):
        """Test that updating status creates a history record."""
        api_client.force_authenticate(user=admin_user)
        
        # Get initial history count
        initial_count = AssetStatusHistory.objects.filter(asset=asset_status.asset).count()
        
        # Update status
        data = {
            'status_type': AssetStatus.EN_MANTENIMIENTO,
            'odometer_reading': 1100.0,
        }
        
        response = api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        
        # Check history was created
        new_count = AssetStatusHistory.objects.filter(asset=asset_status.asset).count()
        assert new_count == initial_count + 1
        
        # Verify history record contains correct data
        latest_history = AssetStatusHistory.objects.filter(asset=asset_status.asset).first()
        assert latest_history.status_type == AssetStatus.OPERANDO  # Old status
        assert latest_history.odometer_reading == 1000.0  # Old reading
    
    def test_history_includes_user_and_timestamp(self, api_client, admin_user, asset_status):
        """Test that history includes user and timestamp."""
        api_client.force_authenticate(user=admin_user)
        
        # Update status
        data = {'status_type': AssetStatus.DETENIDA}
        api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        
        # Check history record
        latest_history = AssetStatusHistory.objects.filter(asset=asset_status.asset).first()
        assert latest_history.updated_by == admin_user
        assert latest_history.timestamp is not None


@pytest.mark.django_db
class TestStatusChangeNotifications:
    """Test status change notifications."""
    
    def test_fuera_de_servicio_creates_alert(self, api_client, admin_user, supervisor_user, asset_status):
        """Test that changing to FUERA_DE_SERVICIO creates alert notification."""
        api_client.force_authenticate(user=admin_user)
        
        # Update to FUERA_DE_SERVICIO
        data = {
            'status_type': AssetStatus.FUERA_DE_SERVICIO,
            'condition_notes': 'Critical failure'
        }
        
        response = api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        
        # Check notifications were created
        from apps.notifications.models import Notification
        notifications = Notification.objects.filter(
            notification_type='ALERT',
            related_object_type='asset',
            related_object_id=asset_status.asset.id
        )
        
        # Should have notifications for admin and supervisor
        assert notifications.count() >= 1


@pytest.mark.django_db
class TestFuelLevelValidation:
    """Test fuel level validation."""
    
    def test_fuel_level_must_be_between_0_and_100(self, api_client, admin_user, asset_status):
        """Test that fuel level must be between 0 and 100."""
        api_client.force_authenticate(user=admin_user)
        
        # Test invalid fuel level (> 100)
        data = {'fuel_level': 150}
        response = api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Test invalid fuel level (< 0)
        data = {'fuel_level': -10}
        response = api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Test valid fuel level
        data = {'fuel_level': 50}
        response = api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestStatusHistoryFiltering:
    """Test status history filtering."""
    
    def test_filter_history_by_asset(self, api_client, admin_user, asset, asset_status):
        """Test filtering history by asset."""
        api_client.force_authenticate(user=admin_user)
        
        # Create some history by updating status
        for i in range(3):
            data = {'odometer_reading': 1000 + (i * 100)}
            api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', data)
        
        # Filter by asset
        response = api_client.get(f'/api/v1/machine-status/history/?asset={asset.id}')
        assert response.status_code == status.HTTP_200_OK
        
        results = response.data.get('results', response.data)
        assert len(results) >= 3
    
    def test_filter_history_by_status_type(self, api_client, admin_user, asset_status):
        """Test filtering history by status type."""
        api_client.force_authenticate(user=admin_user)
        
        # Update to different statuses
        api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', 
                        {'status_type': AssetStatus.EN_MANTENIMIENTO})
        api_client.patch(f'/api/v1/machine-status/status/{asset_status.id}/', 
                        {'status_type': AssetStatus.DETENIDA})
        
        # Filter by status type
        response = api_client.get(f'/api/v1/machine-status/history/?status_type={AssetStatus.OPERANDO}')
        assert response.status_code == status.HTTP_200_OK
        
        results = response.data.get('results', response.data)
        for record in results:
            assert record['status_type'] == AssetStatus.OPERANDO

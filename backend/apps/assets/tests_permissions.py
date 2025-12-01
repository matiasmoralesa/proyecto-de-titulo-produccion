"""
Property-based tests for Assets permissions.

**Feature: permisos-roles, Property 4: Asset Access Consistency**
**Validates: Requirements 2.1**
"""
import pytest
from hypothesis import given, strategies as st, settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.models import Role
from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset, Location

User = get_user_model()


@pytest.fixture
def api_client():
    """Create API client"""
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def setup_roles():
    """Create roles"""
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


def get_token(user):
    """Get JWT token for user"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.mark.django_db
class TestAssetAccessConsistency:
    """
    Property 4: Asset Access Consistency
    
    For any operador user, if they can access a work order,
    they should be able to access the associated asset, and vice versa.
    
    **Feature: permisos-roles, Property 4: Asset Access Consistency**
    **Validates: Requirements 2.1**
    """
    
    def test_operator_can_access_asset_from_work_order(self, api_client, setup_roles):
        """
        Test that if an operator has a work order for an asset,
        they can access that asset.
        """
        from django.utils import timezone
        
        # Create users
        admin = User.objects.create_user(
            username='admin_asset',
            email='admin_asset@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='operator_asset',
            email='op_asset@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        # Create location and asset
        location = Location.objects.create(
            name='Asset Test Location',
            address='123 Asset St'
        )
        
        asset = Asset.objects.create(
            name='Test Asset for Consistency',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model 1',
            serial_number='SN-CONSIST-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Create work order for operator with this asset
        wo = WorkOrder.objects.create(
            title='WO for Asset Test',
            description='Test WO',
            asset=asset,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Test: Operator should be able to access the asset
        token = get_token(operator)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Check if asset appears in list
        response = api_client.get('/api/v1/assets/')
        assert response.status_code == 200
        
        asset_ids = [a['id'] for a in response.data['results']]
        assert asset.id in asset_ids, "Operator should see asset from their work order"
        
        # Check if operator can retrieve asset details
        response = api_client.get(f'/api/v1/assets/{asset.id}/')
        assert response.status_code == 200
        assert response.data['id'] == asset.id
    
    def test_operator_cannot_access_asset_without_work_order(self, api_client, setup_roles):
        """
        Test that if an operator doesn't have a work order for an asset,
        they cannot access that asset.
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_no_wo',
            email='admin_no_wo@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='operator_no_wo',
            email='op_no_wo@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='No WO Location',
            address='456 No WO St'
        )
        
        # Create asset without work order for operator
        asset = Asset.objects.create(
            name='Asset Without WO',
            vehicle_type=Asset.CAMIONETA_MDO,
            model='Model 2',
            serial_number='SN-NO-WO-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Test: Operator should NOT see this asset
        token = get_token(operator)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = api_client.get('/api/v1/assets/')
        assert response.status_code == 200
        
        asset_ids = [a['id'] for a in response.data['results']]
        assert asset.id not in asset_ids, "Operator should not see asset without work order"
        
        # Test: Operator should get 404 when trying to access asset directly
        response = api_client.get(f'/api/v1/assets/{asset.id}/')
        assert response.status_code == 404, "Should return 404 to not reveal existence"
    
    def test_asset_access_consistency_across_multiple_work_orders(self, api_client, setup_roles):
        """
        Test that asset access is consistent when operator has multiple work orders.
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_multi_asset',
            email='admin_multi_asset@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='operator_multi_asset',
            email='op_multi_asset@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Multi Asset Location',
            address='789 Multi St'
        )
        
        # Create 3 assets
        assets = []
        for i in range(3):
            asset = Asset.objects.create(
                name=f'Asset {i}',
                vehicle_type=Asset.RETROEXCAVADORA_MDO,
                model=f'Model {i}',
                serial_number=f'SN-MULTI-{i:03d}',
                location=location,
                status=Asset.STATUS_OPERANDO,
                installation_date=timezone.now().date(),
                created_by=admin
            )
            assets.append(asset)
        
        # Create work orders for assets 0 and 1 only
        for i in range(2):
            WorkOrder.objects.create(
                title=f'WO for Asset {i}',
                description=f'Test WO {i}',
                asset=assets[i],
                assigned_to=operator,
                created_by=admin,
                scheduled_date=timezone.now()
            )
        
        # Test: Operator should see only assets 0 and 1
        token = get_token(operator)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = api_client.get('/api/v1/assets/')
        assert response.status_code == 200
        
        asset_ids = [a['id'] for a in response.data['results']]
        assert assets[0].id in asset_ids
        assert assets[1].id in asset_ids
        assert assets[2].id not in asset_ids, "Should not see asset without work order"
        
        # Verify count
        assert len(asset_ids) == 2
    
    def test_supervisor_sees_all_assets(self, api_client, setup_roles):
        """Test that supervisors can see all assets."""
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_super_asset',
            email='admin_super_asset@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        supervisor = User.objects.create_user(
            username='supervisor_asset',
            email='supervisor_asset@test.com',
            password='testpass123',
            role=setup_roles['supervisor']
        )
        
        operator = User.objects.create_user(
            username='operator_super_asset',
            email='op_super_asset@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Supervisor Asset Location',
            address='321 Super St'
        )
        
        # Create asset with work order for operator
        asset = Asset.objects.create(
            name='Supervisor Test Asset',
            vehicle_type=Asset.CARGADOR_FRONTAL_MDO,
            model='Model Super',
            serial_number='SN-SUPER-ASSET-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        WorkOrder.objects.create(
            title='WO for Supervisor Test',
            description='Test WO',
            asset=asset,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Test: Supervisor should see all assets
        token = get_token(supervisor)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = api_client.get('/api/v1/assets/')
        assert response.status_code == 200
        
        asset_ids = [a['id'] for a in response.data['results']]
        assert asset.id in asset_ids, "Supervisor should see all assets"
    
    def test_admin_sees_all_assets(self, api_client, setup_roles):
        """Test that admins can see all assets."""
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_all_assets',
            email='admin_all_assets@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        location = Location.objects.create(
            name='Admin Asset Location',
            address='654 Admin St'
        )
        
        # Create asset without any work orders
        asset = Asset.objects.create(
            name='Admin Test Asset',
            vehicle_type=Asset.MINICARGADOR_MDO,
            model='Model Admin',
            serial_number='SN-ADMIN-ASSET-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Test: Admin should see all assets
        token = get_token(admin)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = api_client.get('/api/v1/assets/')
        assert response.status_code == 200
        
        asset_ids = [a['id'] for a in response.data['results']]
        assert asset.id in asset_ids, "Admin should see all assets"

"""
Property-based tests for automatic filter application across all endpoints.

**Feature: permisos-roles, Property 7: Automatic Filter Application**
**Validates: Requirements 7.1, 7.2**
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.models import Role
from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset, Location
from apps.ml_predictions.models import FailurePrediction

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
class TestAutomaticFilterApplication:
    """
    Property 7: Automatic Filter Application
    
    For any endpoint that returns a list of resources, the system should
    automatically filter results based on the user's role without requiring
    explicit filtering in the request.
    
    **Feature: permisos-roles, Property 7: Automatic Filter Application**
    **Validates: Requirements 7.1, 7.2**
    """
    
    def test_work_orders_endpoint_filters_automatically(self, api_client, setup_roles):
        """
        Test that work orders endpoint automatically filters by role.
        
        Operators should only see their assigned work orders without
        needing to add any query parameters.
        """
        from django.utils import timezone
        
        # Create users
        admin = User.objects.create_user(
            username='admin_filter',
            email='admin_filter@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator1 = User.objects.create_user(
            username='op1_filter',
            email='op1_filter@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        operator2 = User.objects.create_user(
            username='op2_filter',
            email='op2_filter@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        # Create location and asset
        location = Location.objects.create(
            name='Filter Test Location',
            address='123 Filter St'
        )
        
        asset = Asset.objects.create(
            name='Filter Test Asset',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model 1',
            serial_number='SN-FILTER-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Create work orders for different operators
        wo1 = WorkOrder.objects.create(
            title='WO for Op1',
            description='Test WO 1',
            asset=asset,
            assigned_to=operator1,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        wo2 = WorkOrder.objects.create(
            title='WO for Op2',
            description='Test WO 2',
            asset=asset,
            assigned_to=operator2,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Test: Operator 1 makes request WITHOUT any filters
        token1 = get_token(operator1)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token1}')
        
        # No query parameters - should still be filtered automatically
        response = api_client.get('/api/v1/work-orders/')
        assert response.status_code == 200
        
        # Should only see their own work order
        work_order_ids = [wo['id'] for wo in response.data['results']]
        assert str(wo1.id) in work_order_ids, "Should see own work order"
        assert str(wo2.id) not in work_order_ids, "Should NOT see other operator's work order"
        
        # Verify all returned work orders belong to operator1
        for wo_data in response.data['results']:
            assert wo_data['assigned_to']['id'] == str(operator1.id), \
                "All work orders should be assigned to operator1"
    
    def test_assets_endpoint_filters_automatically(self, api_client, setup_roles):
        """
        Test that assets endpoint automatically filters by role.
        
        Operators should only see assets from their work orders without
        needing to add any query parameters.
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_asset_filter',
            email='admin_asset_filter@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='op_asset_filter',
            email='op_asset_filter@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Asset Filter Location',
            address='456 Asset Filter St'
        )
        
        # Create two assets
        asset1 = Asset.objects.create(
            name='Asset with WO',
            vehicle_type=Asset.CAMIONETA_MDO,
            model='Model 1',
            serial_number='SN-ASSET-FILTER-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        asset2 = Asset.objects.create(
            name='Asset without WO',
            vehicle_type=Asset.RETROEXCAVADORA_MDO,
            model='Model 2',
            serial_number='SN-ASSET-FILTER-002',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Create work order only for asset1
        WorkOrder.objects.create(
            title='WO for Asset1',
            description='Test WO',
            asset=asset1,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Test: Operator makes request WITHOUT any filters
        token = get_token(operator)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = api_client.get('/api/v1/assets/')
        assert response.status_code == 200
        
        # Should only see asset1 (has work order)
        asset_ids = [a['id'] for a in response.data['results']]
        assert str(asset1.id) in asset_ids, "Should see asset with work order"
        assert str(asset2.id) not in asset_ids, "Should NOT see asset without work order"
    
    def test_predictions_endpoint_filters_automatically(self, api_client, setup_roles):
        """
        Test that predictions endpoint automatically filters by role.
        
        Operators should only see predictions for assets they have access to.
        """
        from django.utils import timezone
        from datetime import timedelta
        
        admin = User.objects.create_user(
            username='admin_pred_filter',
            email='admin_pred_filter@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='op_pred_filter',
            email='op_pred_filter@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Prediction Filter Location',
            address='789 Pred Filter St'
        )
        
        # Create two assets
        asset1 = Asset.objects.create(
            name='Asset with Access',
            vehicle_type=Asset.CARGADOR_FRONTAL_MDO,
            model='Model 1',
            serial_number='SN-PRED-FILTER-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        asset2 = Asset.objects.create(
            name='Asset without Access',
            vehicle_type=Asset.MINICARGADOR_MDO,
            model='Model 2',
            serial_number='SN-PRED-FILTER-002',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Create work order only for asset1
        WorkOrder.objects.create(
            title='WO for Asset1',
            description='Test WO',
            asset=asset1,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Create predictions for both assets
        pred1 = FailurePrediction.objects.create(
            asset=asset1,
            failure_probability=0.85,
            risk_level='HIGH',
            model_version='1.0',
            confidence_score=0.85,
            estimated_days_to_failure=7
        )
        
        pred2 = FailurePrediction.objects.create(
            asset=asset2,
            failure_probability=0.90,
            risk_level='CRITICAL',
            model_version='1.0',
            confidence_score=0.90,
            estimated_days_to_failure=5
        )
        
        # Test: Operator makes request WITHOUT any filters
        token = get_token(operator)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = api_client.get('/api/v1/predictions/')
        assert response.status_code == 200
        
        # Should only see prediction for asset1
        prediction_ids = [p['id'] for p in response.data['results']]
        assert str(pred1.id) in prediction_ids, "Should see prediction for accessible asset"
        assert str(pred2.id) not in prediction_ids, "Should NOT see prediction for inaccessible asset"
    
    def test_multiple_endpoints_consistent_filtering(self, api_client, setup_roles):
        """
        Test that filtering is consistent across multiple endpoints.
        
        If an operator can see an asset, they should see:
        - Work orders for that asset
        - Predictions for that asset
        - All related data consistently
        """
        from django.utils import timezone
        from datetime import timedelta
        
        admin = User.objects.create_user(
            username='admin_consistent',
            email='admin_consistent@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='op_consistent',
            email='op_consistent@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Consistent Filter Location',
            address='321 Consistent St'
        )
        
        asset = Asset.objects.create(
            name='Consistent Test Asset',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model Consistent',
            serial_number='SN-CONSISTENT-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Create work order for operator
        wo = WorkOrder.objects.create(
            title='Consistent WO',
            description='Test WO',
            asset=asset,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Create prediction for asset
        pred = FailurePrediction.objects.create(
            asset=asset,
            failure_probability=0.75,
            risk_level='MEDIUM',
            model_version='1.0',
            confidence_score=0.75,
            estimated_days_to_failure=10
        )
        
        # Test: Operator should see consistent data across all endpoints
        token = get_token(operator)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Check assets endpoint
        response = api_client.get('/api/v1/assets/')
        assert response.status_code == 200
        asset_ids = [a['id'] for a in response.data['results']]
        assert str(asset.id) in asset_ids, "Should see asset"
        
        # Check work orders endpoint
        response = api_client.get('/api/v1/work-orders/')
        assert response.status_code == 200
        wo_ids = [w['id'] for w in response.data['results']]
        assert str(wo.id) in wo_ids, "Should see work order for accessible asset"
        
        # Check predictions endpoint
        response = api_client.get('/api/v1/predictions/')
        assert response.status_code == 200
        pred_ids = [p['id'] for p in response.data['results']]
        assert str(pred.id) in pred_ids, "Should see prediction for accessible asset"
    
    def test_supervisor_sees_all_without_filters(self, api_client, setup_roles):
        """
        Test that supervisors see all data without needing filters.
        
        Supervisors should automatically see all work orders, assets, and
        predictions without adding query parameters.
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_super_all',
            email='admin_super_all@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        supervisor = User.objects.create_user(
            username='supervisor_all',
            email='supervisor_all@test.com',
            password='testpass123',
            role=setup_roles['supervisor']
        )
        
        operator = User.objects.create_user(
            username='op_super_all',
            email='op_super_all@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Supervisor All Location',
            address='654 Super All St'
        )
        
        asset = Asset.objects.create(
            name='Supervisor All Asset',
            vehicle_type=Asset.CAMIONETA_MDO,
            model='Model Super',
            serial_number='SN-SUPER-ALL-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Create work order for operator
        wo = WorkOrder.objects.create(
            title='WO for Operator',
            description='Test WO',
            asset=asset,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Test: Supervisor should see all data without filters
        token = get_token(supervisor)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Check work orders
        response = api_client.get('/api/v1/work-orders/')
        assert response.status_code == 200
        wo_ids = [w['id'] for w in response.data['results']]
        assert str(wo.id) in wo_ids, "Supervisor should see all work orders"
        
        # Check assets
        response = api_client.get('/api/v1/assets/')
        assert response.status_code == 200
        asset_ids = [a['id'] for a in response.data['results']]
        assert str(asset.id) in asset_ids, "Supervisor should see all assets"
    
    def test_admin_sees_everything_without_filters(self, api_client, setup_roles):
        """
        Test that admins see everything without needing filters.
        
        Admins should automatically see all resources regardless of
        ownership or assignment.
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_everything',
            email='admin_everything@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='op_everything',
            email='op_everything@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Admin Everything Location',
            address='987 Admin Everything St'
        )
        
        asset = Asset.objects.create(
            name='Admin Everything Asset',
            vehicle_type=Asset.RETROEXCAVADORA_MDO,
            model='Model Admin',
            serial_number='SN-ADMIN-EVERYTHING-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Create work order for operator
        wo = WorkOrder.objects.create(
            title='WO for Operator',
            description='Test WO',
            asset=asset,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Test: Admin should see everything without filters
        token = get_token(admin)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Check work orders
        response = api_client.get('/api/v1/work-orders/')
        assert response.status_code == 200
        wo_ids = [w['id'] for w in response.data['results']]
        assert str(wo.id) in wo_ids, "Admin should see all work orders"
        
        # Check assets
        response = api_client.get('/api/v1/assets/')
        assert response.status_code == 200
        asset_ids = [a['id'] for a in response.data['results']]
        assert str(asset.id) in asset_ids, "Admin should see all assets"
    
    def test_filter_application_without_explicit_parameters(self, api_client, setup_roles):
        """
        Test that filters are applied even when user tries to bypass them.
        
        An operator should not be able to see other operators' data even if
        they try to add query parameters to override the filtering.
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_bypass',
            email='admin_bypass@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator1 = User.objects.create_user(
            username='op1_bypass',
            email='op1_bypass@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        operator2 = User.objects.create_user(
            username='op2_bypass',
            email='op2_bypass@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Bypass Test Location',
            address='111 Bypass St'
        )
        
        asset = Asset.objects.create(
            name='Bypass Test Asset',
            vehicle_type=Asset.CARGADOR_FRONTAL_MDO,
            model='Model Bypass',
            serial_number='SN-BYPASS-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Create work orders for different operators
        wo1 = WorkOrder.objects.create(
            title='WO for Op1',
            description='Test WO 1',
            asset=asset,
            assigned_to=operator1,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        wo2 = WorkOrder.objects.create(
            title='WO for Op2',
            description='Test WO 2',
            asset=asset,
            assigned_to=operator2,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Test: Operator 1 tries to see all work orders with query parameter
        token1 = get_token(operator1)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token1}')
        
        # Try to bypass filter with query parameter
        response = api_client.get(f'/api/v1/work-orders/?assigned_to={operator2.id}')
        assert response.status_code == 200
        
        # Should still only see their own work orders (filter is enforced)
        work_order_ids = [wo['id'] for wo in response.data['results']]
        assert str(wo2.id) not in work_order_ids, "Should NOT see other operator's work order even with query param"
        
        # If any results, they should all belong to operator1
        for wo_data in response.data['results']:
            assert wo_data['assigned_to']['id'] == str(operator1.id), \
                "All work orders should belong to operator1"

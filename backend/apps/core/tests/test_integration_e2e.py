"""
End-to-end integration tests for role-based permissions system.

These tests verify complete user flows from login to resource access,
ensuring that the permission system works correctly across the entire application.
"""
import pytest
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
class TestOperatorE2EFlow:
    """
    End-to-end tests for operator user flows.
    
    These tests verify that operators can only access their assigned resources
    and are properly denied access to resources belonging to other operators.
    """
    
    def test_operator_login_and_access_own_work_order(self, api_client, setup_roles):
        """
        Test complete flow: operator logs in and accesses their work order.
        
        Flow:
        1. Create operator user
        2. Create work order assigned to operator
        3. Login as operator (get token)
        4. Access work order list
        5. Verify operator sees their work order
        6. Access specific work order detail
        7. Verify operator can view their work order details
        """
        from django.utils import timezone
        
        # Setup: Create users and resources
        admin = User.objects.create_user(
            username='admin_e2e',
            email='admin_e2e@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='operator_e2e',
            email='operator_e2e@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='E2E Test Location',
            address='123 E2E St'
        )
        
        asset = Asset.objects.create(
            name='E2E Test Asset',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model 1',
            serial_number='SN-E2E-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        wo = WorkOrder.objects.create(
            title='E2E Test WO',
            description='Test work order for E2E',
            asset=asset,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Step 1: Login as operator (get token)
        token = get_token(operator)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Step 2: Access work order list
        response = api_client.get('/api/v1/work-orders/')
        assert response.status_code == 200, "Operator should be able to access work orders list"
        
        # Step 3: Verify operator sees their work order
        work_order_ids = [w['id'] for w in response.data['results']]
        assert str(wo.id) in work_order_ids, "Operator should see their assigned work order"
        
        # Step 4: Access specific work order detail
        response = api_client.get(f'/api/v1/work-orders/{wo.id}/')
        assert response.status_code == 200, "Operator should be able to view their work order details"
        assert response.data['id'] == str(wo.id), "Work order ID should match"
        assert response.data['title'] == wo.title, "Work order title should match"
    
    def test_operator_denied_access_to_other_work_order(self, api_client, setup_roles):
        """
        Test complete flow: operator tries to access another operator's work order and is denied.
        
        Flow:
        1. Create two operators
        2. Create work orders for each operator
        3. Login as operator1
        4. Try to access operator2's work order
        5. Verify access is denied (404)
        6. Try to access work order list
        7. Verify operator1 only sees their own work order
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_deny',
            email='admin_deny@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator1 = User.objects.create_user(
            username='operator1_deny',
            email='op1_deny@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        operator2 = User.objects.create_user(
            username='operator2_deny',
            email='op2_deny@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Deny Test Location',
            address='456 Deny St'
        )
        
        asset = Asset.objects.create(
            name='Deny Test Asset',
            vehicle_type=Asset.CAMIONETA_MDO,
            model='Model 2',
            serial_number='SN-DENY-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        wo1 = WorkOrder.objects.create(
            title='WO for Operator 1',
            description='Test WO 1',
            asset=asset,
            assigned_to=operator1,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        wo2 = WorkOrder.objects.create(
            title='WO for Operator 2',
            description='Test WO 2',
            asset=asset,
            assigned_to=operator2,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Login as operator1
        token = get_token(operator1)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Try to access operator2's work order directly
        response = api_client.get(f'/api/v1/work-orders/{wo2.id}/')
        assert response.status_code == 404, "Operator should get 404 when accessing other operator's work order"
        
        # Access work order list
        response = api_client.get('/api/v1/work-orders/')
        assert response.status_code == 200
        
        # Verify operator1 only sees their own work order
        work_order_ids = [w['id'] for w in response.data['results']]
        assert str(wo1.id) in work_order_ids, "Operator should see their own work order"
        assert str(wo2.id) not in work_order_ids, "Operator should NOT see other operator's work order"


@pytest.mark.django_db
class TestSupervisorE2EFlow:
    """
    End-to-end tests for supervisor user flows.
    
    These tests verify that supervisors can access all work orders
    and have appropriate permissions across the system.
    """
    
    def test_supervisor_login_and_view_all_work_orders(self, api_client, setup_roles):
        """
        Test complete flow: supervisor logs in and views all work orders.
        
        Flow:
        1. Create supervisor and operators
        2. Create work orders for different operators
        3. Login as supervisor
        4. Access work order list
        5. Verify supervisor sees all work orders
        6. Access specific work order details
        7. Verify supervisor can view any work order
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_super_e2e',
            email='admin_super_e2e@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        supervisor = User.objects.create_user(
            username='supervisor_e2e',
            email='supervisor_e2e@test.com',
            password='testpass123',
            role=setup_roles['supervisor']
        )
        
        operator1 = User.objects.create_user(
            username='op1_super_e2e',
            email='op1_super_e2e@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        operator2 = User.objects.create_user(
            username='op2_super_e2e',
            email='op2_super_e2e@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Supervisor E2E Location',
            address='789 Super E2E St'
        )
        
        asset = Asset.objects.create(
            name='Supervisor E2E Asset',
            vehicle_type=Asset.RETROEXCAVADORA_MDO,
            model='Model 3',
            serial_number='SN-SUPER-E2E-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
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
        
        # Login as supervisor
        token = get_token(supervisor)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Access work order list
        response = api_client.get('/api/v1/work-orders/')
        assert response.status_code == 200, "Supervisor should be able to access work orders list"
        
        # Verify supervisor sees all work orders
        work_order_ids = [w['id'] for w in response.data['results']]
        assert str(wo1.id) in work_order_ids, "Supervisor should see operator1's work order"
        assert str(wo2.id) in work_order_ids, "Supervisor should see operator2's work order"
        
        # Access specific work order details
        response = api_client.get(f'/api/v1/work-orders/{wo1.id}/')
        assert response.status_code == 200, "Supervisor should be able to view any work order details"
        
        response = api_client.get(f'/api/v1/work-orders/{wo2.id}/')
        assert response.status_code == 200, "Supervisor should be able to view any work order details"


@pytest.mark.django_db
class TestAdminE2EFlow:
    """
    End-to-end tests for admin user flows.
    
    These tests verify that admins have full access to all resources
    and can perform all operations.
    """
    
    def test_admin_login_and_full_access(self, api_client, setup_roles):
        """
        Test complete flow: admin logs in and has full access to all resources.
        
        Flow:
        1. Create admin and operators
        2. Create work orders for operators
        3. Login as admin
        4. Access work order list
        5. Verify admin sees all work orders
        6. Access any work order details
        7. Verify admin can view and modify any resource
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_full',
            email='admin_full@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='op_admin_full',
            email='op_admin_full@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Admin Full Location',
            address='321 Admin Full St'
        )
        
        asset = Asset.objects.create(
            name='Admin Full Asset',
            vehicle_type=Asset.CARGADOR_FRONTAL_MDO,
            model='Model 4',
            serial_number='SN-ADMIN-FULL-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        wo = WorkOrder.objects.create(
            title='WO for Admin Test',
            description='Test WO',
            asset=asset,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Login as admin
        token = get_token(admin)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Access work order list
        response = api_client.get('/api/v1/work-orders/')
        assert response.status_code == 200, "Admin should be able to access work orders list"
        
        # Verify admin sees all work orders
        work_order_ids = [w['id'] for w in response.data['results']]
        assert str(wo.id) in work_order_ids, "Admin should see all work orders"
        
        # Access specific work order details
        response = api_client.get(f'/api/v1/work-orders/{wo.id}/')
        assert response.status_code == 200, "Admin should be able to view any work order details"
        assert response.data['id'] == str(wo.id), "Work order ID should match"


@pytest.mark.django_db
class TestCrossResourceE2EFlow:
    """
    End-to-end tests for cross-resource access patterns.
    
    These tests verify that permissions are consistent across related resources
    (work orders, assets, predictions).
    """
    
    def test_operator_asset_access_consistency(self, api_client, setup_roles):
        """
        Test that operator's access to assets is consistent with work order access.
        
        Flow:
        1. Create operator with work order for specific asset
        2. Login as operator
        3. Verify operator can access the asset
        4. Create another asset without work order
        5. Verify operator cannot access the other asset
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_asset_consistency',
            email='admin_asset_consistency@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='op_asset_consistency',
            email='op_asset_consistency@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Asset Consistency Location',
            address='654 Consistency St'
        )
        
        # Asset with work order
        asset_with_wo = Asset.objects.create(
            name='Asset With WO',
            vehicle_type=Asset.MINICARGADOR_MDO,
            model='Model 5',
            serial_number='SN-WITH-WO-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Asset without work order
        asset_without_wo = Asset.objects.create(
            name='Asset Without WO',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model 6',
            serial_number='SN-WITHOUT-WO-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Create work order for first asset
        wo = WorkOrder.objects.create(
            title='WO for Asset Consistency',
            description='Test WO',
            asset=asset_with_wo,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Login as operator
        token = get_token(operator)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Verify operator can access asset with work order
        response = api_client.get(f'/api/v1/assets/{asset_with_wo.id}/')
        assert response.status_code == 200, "Operator should be able to access asset from their work order"
        
        # Verify operator cannot access asset without work order
        response = api_client.get(f'/api/v1/assets/{asset_without_wo.id}/')
        assert response.status_code == 404, "Operator should NOT be able to access asset without work order"
    
    def test_permission_consistency_across_endpoints(self, api_client, setup_roles):
        """
        Test that permissions are consistently applied across all endpoints.
        
        Flow:
        1. Create operator with work order
        2. Login as operator
        3. Verify consistent access across work orders, assets endpoints
        4. Verify consistent denial of access to unauthorized resources
        """
        from django.utils import timezone
        
        admin = User.objects.create_user(
            username='admin_consistency',
            email='admin_consistency@test.com',
            password='testpass123',
            role=setup_roles['admin']
        )
        
        operator = User.objects.create_user(
            username='op_consistency',
            email='op_consistency@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        other_operator = User.objects.create_user(
            username='other_op_consistency',
            email='other_op_consistency@test.com',
            password='testpass123',
            role=setup_roles['operator']
        )
        
        location = Location.objects.create(
            name='Consistency Test Location',
            address='987 Consistency St'
        )
        
        asset = Asset.objects.create(
            name='Consistency Test Asset',
            vehicle_type=Asset.CAMIONETA_MDO,
            model='Model 7',
            serial_number='SN-CONSISTENCY-001',
            location=location,
            status=Asset.STATUS_OPERANDO,
            installation_date=timezone.now().date(),
            created_by=admin
        )
        
        # Work order for operator
        wo_operator = WorkOrder.objects.create(
            title='WO for Operator',
            description='Test WO',
            asset=asset,
            assigned_to=operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Work order for other operator
        wo_other = WorkOrder.objects.create(
            title='WO for Other Operator',
            description='Test WO',
            asset=asset,
            assigned_to=other_operator,
            created_by=admin,
            scheduled_date=timezone.now()
        )
        
        # Login as operator
        token = get_token(operator)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Test work orders endpoint
        response = api_client.get('/api/v1/work-orders/')
        assert response.status_code == 200
        work_order_ids = [w['id'] for w in response.data['results']]
        assert str(wo_operator.id) in work_order_ids, "Should see own work order"
        assert str(wo_other.id) not in work_order_ids, "Should NOT see other's work order"
        
        # Test direct access to own work order
        response = api_client.get(f'/api/v1/work-orders/{wo_operator.id}/')
        assert response.status_code == 200, "Should access own work order"
        
        # Test direct access to other's work order
        response = api_client.get(f'/api/v1/work-orders/{wo_other.id}/')
        assert response.status_code == 404, "Should NOT access other's work order"
        
        # Test assets endpoint
        response = api_client.get(f'/api/v1/assets/{asset.id}/')
        assert response.status_code == 200, "Should access asset from own work order"

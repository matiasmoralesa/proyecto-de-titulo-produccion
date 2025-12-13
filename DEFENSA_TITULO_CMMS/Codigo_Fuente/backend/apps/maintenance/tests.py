"""
Tests for maintenance app.
"""
from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from apps.maintenance.models import MaintenancePlan
from apps.assets.models import Asset, Location
from apps.authentication.models import User, Role


class MaintenancePlanModelTest(TestCase):
    """Test MaintenancePlan model."""
    
    def setUp(self):
        """Set up test data."""
        # Create role
        self.admin_role = Role.objects.create(
            name='ADMIN',
            description='Administrator'
        )
        
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role=self.admin_role
        )
        
        # Create location
        self.location = Location.objects.create(
            name='Test Location'
        )
        
        # Create asset
        self.asset = Asset.objects.create(
            name='Test Asset',
            vehicle_type='Camión Supersucker',
            model='Test Model',
            serial_number='TEST123',
            location=self.location,
            installation_date=date.today(),
            created_by=self.user
        )
    
    def test_create_monthly_plan(self):
        """Test creating a monthly maintenance plan."""
        plan = MaintenancePlan.objects.create(
            name='Monthly Maintenance',
            description='Test monthly maintenance',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_MONTHLY,
            recurrence_interval=1,
            start_date=date.today(),
            created_by=self.user
        )
        
        self.assertEqual(plan.name, 'Monthly Maintenance')
        self.assertEqual(plan.status, MaintenancePlan.STATUS_ACTIVE)
        self.assertIsNotNone(plan.next_due_date)
        self.assertFalse(plan.is_paused)
    
    def test_calculate_next_due_date_monthly(self):
        """Test next due date calculation for monthly recurrence."""
        plan = MaintenancePlan.objects.create(
            name='Monthly Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_MONTHLY,
            recurrence_interval=1,
            start_date=date.today(),
            created_by=self.user
        )
        
        expected_date = date.today() + timedelta(days=30)
        # Allow 2 days tolerance for month length variations
        self.assertAlmostEqual(
            (plan.next_due_date - expected_date).days,
            0,
            delta=2
        )
    
    def test_calculate_next_due_date_weekly(self):
        """Test next due date calculation for weekly recurrence."""
        plan = MaintenancePlan.objects.create(
            name='Weekly Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_WEEKLY,
            recurrence_interval=1,
            start_date=date.today(),
            created_by=self.user
        )
        
        expected_date = date.today() + timedelta(weeks=1)
        self.assertEqual(plan.next_due_date, expected_date)
    
    def test_usage_based_plan(self):
        """Test usage-based maintenance plan."""
        plan = MaintenancePlan.objects.create(
            name='Usage Based Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_HOURS,
            recurrence_interval=1,
            start_date=date.today(),
            usage_threshold=100,
            last_usage_value=50,
            created_by=self.user
        )
        
        self.assertTrue(plan.is_usage_based())
        self.assertIsNone(plan.next_due_date)
        self.assertEqual(plan.usage_until_due(), 50)
    
    def test_is_due_time_based(self):
        """Test is_due for time-based plans."""
        # Create plan with past due date
        plan = MaintenancePlan.objects.create(
            name='Past Due Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_DAILY,
            recurrence_interval=1,
            start_date=date.today() - timedelta(days=5),
            created_by=self.user
        )
        
        # Manually set next_due_date to past
        plan.next_due_date = date.today() - timedelta(days=1)
        plan.save()
        
        self.assertTrue(plan.is_due())
        self.assertTrue(plan.is_overdue())
    
    def test_is_due_usage_based(self):
        """Test is_due for usage-based plans."""
        plan = MaintenancePlan.objects.create(
            name='Usage Due Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_HOURS,
            recurrence_interval=1,
            start_date=date.today(),
            usage_threshold=100,
            last_usage_value=100,
            created_by=self.user
        )
        
        self.assertTrue(plan.is_due())
    
    def test_pause_resume(self):
        """Test pausing and resuming a plan."""
        plan = MaintenancePlan.objects.create(
            name='Pause Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_MONTHLY,
            recurrence_interval=1,
            start_date=date.today(),
            created_by=self.user
        )
        
        # Pause
        plan.pause(self.user)
        self.assertTrue(plan.is_paused)
        self.assertEqual(plan.status, MaintenancePlan.STATUS_PAUSED)
        self.assertIsNotNone(plan.paused_at)
        self.assertEqual(plan.paused_by, self.user)
        
        # Resume
        plan.resume()
        self.assertFalse(plan.is_paused)
        self.assertEqual(plan.status, MaintenancePlan.STATUS_ACTIVE)
        self.assertIsNone(plan.paused_at)
        self.assertIsNone(plan.paused_by)
    
    def test_complete_maintenance(self):
        """Test completing maintenance."""
        plan = MaintenancePlan.objects.create(
            name='Complete Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_MONTHLY,
            recurrence_interval=1,
            start_date=date.today() - timedelta(days=30),
            created_by=self.user
        )
        
        original_next_due = plan.next_due_date
        completion_date = date.today()
        
        plan.complete_maintenance(completion_date=completion_date)
        
        self.assertEqual(plan.last_completed_date, completion_date)
        # Next due should be calculated from completion date
        expected_next_due = completion_date + timedelta(days=30)
        self.assertAlmostEqual(
            (plan.next_due_date - expected_next_due).days,
            0,
            delta=2
        )
        self.assertIsNotNone(plan.next_due_date)
    
    def test_update_usage(self):
        """Test updating usage value."""
        plan = MaintenancePlan.objects.create(
            name='Update Usage Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_KILOMETERS,
            recurrence_interval=1,
            start_date=date.today(),
            usage_threshold=5000,
            last_usage_value=1000,
            created_by=self.user
        )
        
        plan.update_usage(3000)
        self.assertEqual(plan.last_usage_value, 3000)
        self.assertEqual(plan.usage_until_due(), 2000)
    
    def test_days_until_due(self):
        """Test days_until_due calculation."""
        plan = MaintenancePlan.objects.create(
            name='Days Until Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_WEEKLY,
            recurrence_interval=1,
            start_date=date.today(),
            created_by=self.user
        )
        
        days = plan.days_until_due()
        self.assertIsNotNone(days)
        self.assertEqual(days, 7)
    
    def test_paused_plan_not_due(self):
        """Test that paused plans are not considered due."""
        plan = MaintenancePlan.objects.create(
            name='Paused Not Due Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_DAILY,
            recurrence_interval=1,
            start_date=date.today() - timedelta(days=5),
            created_by=self.user
        )
        
        # Set to past due
        plan.next_due_date = date.today() - timedelta(days=1)
        plan.save()
        
        # Pause the plan
        plan.pause(self.user)
        
        # Should not be due when paused
        self.assertFalse(plan.is_due())


class MaintenancePlanAPITest(TestCase):
    """Test MaintenancePlan API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        from rest_framework.test import APIClient
        
        # Create role
        self.admin_role = Role.objects.create(
            name='ADMIN',
            description='Administrator'
        )
        
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role=self.admin_role
        )
        
        # Create location
        self.location = Location.objects.create(
            name='Test Location'
        )
        
        # Create asset
        self.asset = Asset.objects.create(
            name='Test Asset',
            vehicle_type='Camión Supersucker',
            model='Test Model',
            serial_number='TEST123',
            location=self.location,
            installation_date=date.today(),
            created_by=self.user
        )
        
        # Use APIClient with authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_create_plan_api(self):
        """Test creating a plan via API."""
        data = {
            'name': 'API Test Plan',
            'description': 'Test description',
            'asset': str(self.asset.id),
            'recurrence_type': 'Mensual',
            'recurrence_interval': 1,
            'start_date': date.today().isoformat(),
            'status': 'Activo'
        }
        
        response = self.client.post(
            '/api/v1/maintenance/plans/',
            data=data,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(MaintenancePlan.objects.count(), 1)
        
        plan = MaintenancePlan.objects.first()
        self.assertEqual(plan.name, 'API Test Plan')
        self.assertEqual(plan.created_by, self.user)
    
    def test_list_plans_api(self):
        """Test listing plans via API."""
        MaintenancePlan.objects.create(
            name='Test Plan 1',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_MONTHLY,
            recurrence_interval=1,
            start_date=date.today(),
            created_by=self.user
        )
        
        response = self.client.get('/api/v1/maintenance/plans/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())
        self.assertEqual(len(response.json()['results']), 1)
    
    def test_pause_resume_api(self):
        """Test pause/resume via API."""
        plan = MaintenancePlan.objects.create(
            name='Pause API Test',
            description='Test',
            asset=self.asset,
            recurrence_type=MaintenancePlan.RECURRENCE_MONTHLY,
            recurrence_interval=1,
            start_date=date.today(),
            created_by=self.user
        )
        
        # Pause
        response = self.client.post(
            f'/api/v1/maintenance/plans/{plan.id}/pause_resume/',
            data={'action': 'pause'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        plan.refresh_from_db()
        self.assertTrue(plan.is_paused)
        
        # Resume
        response = self.client.post(
            f'/api/v1/maintenance/plans/{plan.id}/pause_resume/',
            data={'action': 'resume'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        plan.refresh_from_db()
        self.assertFalse(plan.is_paused)

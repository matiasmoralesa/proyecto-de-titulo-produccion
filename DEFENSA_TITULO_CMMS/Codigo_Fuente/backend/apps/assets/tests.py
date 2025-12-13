"""
Tests for assets app.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from .models import Location, Asset, AssetDocument


@pytest.mark.django_db
class TestLocationModel:
    """Tests for Location model."""
    
    def test_create_location(self):
        """Test creating a location."""
        location = Location.objects.create(
            name='Test Location',
            address='Test Address 123',
            coordinates='-12.0464,-77.0428',
            description='Test description'
        )
        
        assert location.name == 'Test Location'
        assert location.address == 'Test Address 123'
        assert str(location) == 'Test Location'
    
    def test_location_unique_name(self):
        """Test that location names must be unique."""
        Location.objects.create(name='Unique Location')
        
        with pytest.raises(Exception):
            Location.objects.create(name='Unique Location')


@pytest.mark.django_db
class TestAssetModel:
    """Tests for Asset model."""
    
    def test_create_asset(self, admin_user):
        """Test creating an asset."""
        location = Location.objects.create(name='Test Location')
        
        asset = Asset.objects.create(
            name='Test Asset',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model X',
            serial_number='SN-12345',
            license_plate='ABC-123',
            location=location,
            installation_date='2024-01-01',
            status=Asset.STATUS_OPERANDO,
            created_by=admin_user
        )
        
        assert asset.name == 'Test Asset'
        assert asset.vehicle_type == Asset.CAMION_SUPERSUCKER
        assert asset.serial_number == 'SN-12345'
        assert asset.is_archived is False
    
    def test_asset_soft_delete(self, admin_user):
        """Test soft delete functionality."""
        location = Location.objects.create(name='Test Location')
        asset = Asset.objects.create(
            name='Test Asset',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model X',
            serial_number='SN-12345',
            location=location,
            installation_date='2024-01-01',
            created_by=admin_user
        )
        
        asset.soft_delete()
        asset.refresh_from_db()
        
        assert asset.is_archived is True
    
    def test_asset_unique_serial_number(self, admin_user):
        """Test that serial numbers must be unique."""
        location = Location.objects.create(name='Test Location')
        
        Asset.objects.create(
            name='Asset 1',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model X',
            serial_number='SN-UNIQUE',
            location=location,
            installation_date='2024-01-01',
            created_by=admin_user
        )
        
        with pytest.raises(Exception):
            Asset.objects.create(
                name='Asset 2',
                vehicle_type=Asset.CAMIONETA_MDO,
                model='Model Y',
                serial_number='SN-UNIQUE',
                location=location,
                installation_date='2024-01-01',
                created_by=admin_user
            )


@pytest.mark.django_db
class TestLocationAPI:
    """Tests for Location API endpoints."""
    
    def test_list_locations(self, authenticated_client):
        """Test listing locations."""
        Location.objects.create(name='Location 1')
        Location.objects.create(name='Location 2')
        
        url = reverse('assets:location-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_create_location_admin_only(self, api_client, admin_user, operador_user):
        """Test that only admins can create locations."""
        url = reverse('assets:location-list')
        data = {'name': 'New Location', 'address': 'Test Address'}
        
        # Admin can create
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Operador cannot create
        api_client.force_authenticate(user=operador_user)
        response = api_client.post(url, {'name': 'Another Location'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_location_with_assets(self, authenticated_client, admin_user):
        """Test that locations with assets cannot be deleted."""
        location = Location.objects.create(name='Location with Assets')
        Asset.objects.create(
            name='Test Asset',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model X',
            serial_number='SN-123',
            location=location,
            installation_date='2024-01-01',
            created_by=admin_user
        )
        
        url = reverse('assets:location-detail', args=[location.id])
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAssetAPI:
    """Tests for Asset API endpoints."""
    
    def test_list_assets(self, authenticated_client, admin_user):
        """Test listing assets."""
        location = Location.objects.create(name='Test Location')
        Asset.objects.create(
            name='Asset 1',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model X',
            serial_number='SN-001',
            location=location,
            installation_date='2024-01-01',
            created_by=admin_user
        )
        
        url = reverse('assets:asset-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_create_asset(self, authenticated_client, admin_user):
        """Test creating an asset."""
        location = Location.objects.create(name='Test Location')
        
        url = reverse('assets:asset-list')
        data = {
            'name': 'New Asset',
            'vehicle_type': Asset.CAMION_SUPERSUCKER,
            'model': 'Model X',
            'serial_number': 'SN-NEW',
            'license_plate': 'XYZ-789',
            'location': str(location.id),
            'installation_date': '2024-01-01',
            'status': Asset.STATUS_OPERANDO
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Asset'
    
    def test_soft_delete_asset(self, authenticated_client, admin_user):
        """Test soft deleting an asset."""
        location = Location.objects.create(name='Test Location')
        asset = Asset.objects.create(
            name='Asset to Delete',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model X',
            serial_number='SN-DELETE',
            location=location,
            installation_date='2024-01-01',
            created_by=admin_user
        )
        
        url = reverse('assets:asset-detail', args=[asset.id])
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify asset is archived
        asset.refresh_from_db()
        assert asset.is_archived is True
    
    def test_filter_assets_by_vehicle_type(self, authenticated_client, admin_user):
        """Test filtering assets by vehicle type."""
        location = Location.objects.create(name='Test Location')
        
        Asset.objects.create(
            name='Truck',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model X',
            serial_number='SN-TRUCK',
            location=location,
            installation_date='2024-01-01',
            created_by=admin_user
        )
        
        Asset.objects.create(
            name='Van',
            vehicle_type=Asset.CAMIONETA_MDO,
            model='Model Y',
            serial_number='SN-VAN',
            location=location,
            installation_date='2024-01-01',
            created_by=admin_user
        )
        
        url = reverse('assets:asset-list')
        response = authenticated_client.get(url, {'vehicle_type': Asset.CAMION_SUPERSUCKER})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['vehicle_type'] == Asset.CAMION_SUPERSUCKER


@pytest.mark.property
@pytest.mark.django_db
class TestAssetUniqueIdentifiers:
    """Property-based test for unique asset identifiers."""
    
    def test_unique_serial_numbers(self, admin_user):
        """
        **Feature: cmms-local, Property 1: Unique Asset Identifiers**
        
        For any two Assets in the system, their serial numbers and license plates
        (if present) must be unique.
        
        **Validates: Requirements 1.5**
        """
        location = Location.objects.create(name='Test Location')
        
        # Create first asset
        asset1 = Asset.objects.create(
            name='Asset 1',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model X',
            serial_number='SN-UNIQUE-1',
            license_plate='PLATE-1',
            location=location,
            installation_date='2024-01-01',
            created_by=admin_user
        )
        
        # Try to create second asset with same serial number
        with pytest.raises(Exception):
            Asset.objects.create(
                name='Asset 2',
                vehicle_type=Asset.CAMIONETA_MDO,
                model='Model Y',
                serial_number='SN-UNIQUE-1',  # Duplicate
                license_plate='PLATE-2',
                location=location,
                installation_date='2024-01-01',
                created_by=admin_user
            )
        
        # Try to create second asset with same license plate
        with pytest.raises(Exception):
            Asset.objects.create(
                name='Asset 3',
                vehicle_type=Asset.RETROEXCAVADORA_MDO,
                model='Model Z',
                serial_number='SN-UNIQUE-3',
                license_plate='PLATE-1',  # Duplicate
                location=location,
                installation_date='2024-01-01',
                created_by=admin_user
            )


@pytest.mark.property
@pytest.mark.django_db
class TestAssetArchival:
    """Property-based test for asset archival."""
    
    def test_asset_archival_instead_of_deletion(self, authenticated_client, admin_user):
        """
        **Feature: cmms-local, Property 9: Asset Archival Instead of Deletion**
        
        For any Asset deletion request, the Asset must be marked as archived
        (is_archived=True) rather than being permanently deleted from the database.
        
        **Validates: Requirements 1.6**
        """
        location = Location.objects.create(name='Test Location')
        asset = Asset.objects.create(
            name='Asset to Archive',
            vehicle_type=Asset.CAMION_SUPERSUCKER,
            model='Model X',
            serial_number='SN-ARCHIVE',
            location=location,
            installation_date='2024-01-01',
            created_by=admin_user
        )
        
        asset_id = asset.id
        
        # Delete the asset via API
        url = reverse('assets:asset-detail', args=[asset_id])
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify asset still exists in database but is archived
        asset = Asset.objects.get(id=asset_id)
        assert asset.is_archived is True

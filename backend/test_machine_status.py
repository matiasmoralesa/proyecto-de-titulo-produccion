"""
Test script for machine status API endpoints.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_machine_status():
    """Test machine status endpoints."""
    
    print("="*50)
    print("Testing Machine Status API")
    print("="*50)
    
    # 1. Login as admin
    print("\n1. Logging in as admin...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login/",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return
    
    token = login_response.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")
    
    # 2. Get list of assets
    print("\n2. Getting list of assets...")
    assets_response = requests.get(
        f"{BASE_URL}/assets/assets/",
        headers=headers
    )
    
    if assets_response.status_code == 200:
        assets_data = assets_response.json()
        assets = assets_data.get('results', assets_data)
        if len(assets) > 0:
            asset_id = assets[0]['id']
            asset_name = assets[0]['name']
            print(f"✅ Found {len(assets)} assets")
            print(f"   Using asset: {asset_name} (ID: {asset_id})")
        else:
            print("❌ No assets found")
            return
    else:
        print(f"❌ Failed to get assets: {assets_response.status_code}")
        return
    
    # 3. Get or create initial status for asset
    print("\n3. Getting or creating initial status for asset...")
    
    # First try to get existing status
    get_status_response = requests.get(
        f"{BASE_URL}/machine-status/status/?asset={asset_id}",
        headers=headers
    )
    
    if get_status_response.status_code == 200:
        status_data_response = get_status_response.json()
        statuses = status_data_response.get('results', status_data_response)
        
        if len(statuses) > 0:
            # Use existing status
            status = statuses[0]
            status_id = status['id']
            print(f"✅ Found existing status: {status['status_type_display']}")
            print(f"   Odometer: {status.get('odometer_reading', 'N/A')}")
            print(f"   Fuel: {status.get('fuel_level', 'N/A')}%")
        else:
            # Create new status
            status_data = {
                "asset": asset_id,
                "status_type": "OPERANDO",
                "odometer_reading": "1000.50",
                "fuel_level": 80,
                "condition_notes": "Asset in good condition"
            }
            
            create_response = requests.post(
                f"{BASE_URL}/machine-status/status/",
                headers=headers,
                json=status_data
            )
            
            if create_response.status_code == 201:
                status = create_response.json()
                status_id = status['id']
                print(f"✅ Status created: {status['status_type_display']}")
                print(f"   Odometer: {status['odometer_reading']}")
                print(f"   Fuel: {status['fuel_level']}%")
            else:
                print(f"❌ Failed to create status: {create_response.status_code}")
                print(create_response.json())
                return
    else:
        print(f"❌ Failed to get status: {get_status_response.status_code}")
        return
    
    # 4. Update status
    print("\n4. Updating asset status...")
    update_data = {
        "status_type": "EN_MANTENIMIENTO",
        "odometer_reading": "1050.75",
        "fuel_level": 60,
        "condition_notes": "Scheduled maintenance"
    }
    
    update_response = requests.patch(
        f"{BASE_URL}/machine-status/status/{status_id}/",
        headers=headers,
        json=update_data
    )
    
    if update_response.status_code == 200:
        updated_status = update_response.json()
        print(f"✅ Status updated: {updated_status.get('status_type_display', updated_status['status_type'])}")
        print(f"   Odometer: {updated_status['odometer_reading']}")
        print(f"   Fuel: {updated_status['fuel_level']}%")
    else:
        print(f"❌ Failed to update status: {update_response.status_code}")
        print(update_response.json())
    
    # 5. Get status history
    print("\n5. Getting status history...")
    history_response = requests.get(
        f"{BASE_URL}/machine-status/history/?asset={asset_id}",
        headers=headers
    )
    
    if history_response.status_code == 200:
        history_data = history_response.json()
        history = history_data.get('results', history_data)
        print(f"✅ Found {len(history)} history records")
        for record in history:
            print(f"   - {record['status_type']} at {record['timestamp']}")
    else:
        print(f"❌ Failed to get history: {history_response.status_code}")
    
    # 6. Update to FUERA_DE_SERVICIO (should create alert)
    print("\n6. Updating status to FUERA_DE_SERVICIO...")
    alert_data = {
        "status_type": "FUERA_DE_SERVICIO",
        "condition_notes": "Critical failure - needs immediate attention"
    }
    
    alert_response = requests.patch(
        f"{BASE_URL}/machine-status/status/{status_id}/",
        headers=headers,
        json=alert_data
    )
    
    if alert_response.status_code == 200:
        print("✅ Status updated to FUERA_DE_SERVICIO")
        print("   Alert notification should be created for ADMIN/SUPERVISOR")
    else:
        print(f"❌ Failed to update status: {alert_response.status_code}")
    
    # 7. Check notifications
    print("\n7. Checking notifications...")
    notif_response = requests.get(
        f"{BASE_URL}/notifications/notifications/",
        headers=headers
    )
    
    if notif_response.status_code == 200:
        notif_data = notif_response.json()
        notifications = notif_data.get('results', notif_data)
        alert_notifs = [n for n in notifications if n['notification_type'] == 'ALERT']
        print(f"✅ Found {len(alert_notifs)} alert notifications")
        if len(alert_notifs) > 0:
            print(f"   Latest: {alert_notifs[0]['title']}")
    else:
        print(f"⚠️  Could not check notifications: {notif_response.status_code}")
    
    # 8. Filter status by type
    print("\n8. Filtering status by type...")
    filter_response = requests.get(
        f"{BASE_URL}/machine-status/status/?status_type=FUERA_DE_SERVICIO",
        headers=headers
    )
    
    if filter_response.status_code == 200:
        filter_data = filter_response.json()
        filtered = filter_data.get('results', filter_data)
        print(f"✅ Found {len(filtered)} assets with FUERA_DE_SERVICIO status")
    else:
        print(f"❌ Failed to filter: {filter_response.status_code}")
    
    print("\n" + "="*50)
    print("Machine Status API Tests Completed!")
    print("="*50)


if __name__ == "__main__":
    test_machine_status()

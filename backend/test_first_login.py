"""
Test script for first login password change flow.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/auth"

def test_first_login_flow():
    """Test first login password change flow."""
    
    print("="*50)
    print("Testing First Login Password Change Flow")
    print("="*50)
    
    # 1. Login as admin
    print("\n1. Logging in as admin...")
    login_response = requests.post(
        f"{BASE_URL}/login/",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return
    
    admin_token = login_response.json()['access']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("✅ Admin login successful")
    
    # 2. Create a test user with must_change_password=True
    print("\n2. Creating test user with must_change_password=True...")
    new_user_data = {
        "username": "test_first_login",
        "email": "test_first_login@example.com",
        "password": "TempPass123!",
        "password_confirm": "TempPass123!",
        "first_name": "Test",
        "last_name": "FirstLogin",
        "role": 3  # OPERADOR
    }
    
    create_response = requests.post(
        f"{BASE_URL}/user-management/",
        headers=admin_headers,
        json=new_user_data
    )
    
    if create_response.status_code == 201:
        new_user = create_response.json()
        print(f"✅ User created: {new_user['username']}")
        print(f"   must_change_password: {new_user['must_change_password']}")
    else:
        print(f"❌ Failed to create user: {create_response.status_code}")
        print(create_response.json())
        return
    
    # 3. Login as the new user
    print("\n3. Logging in as new user...")
    user_login_response = requests.post(
        f"{BASE_URL}/login/",
        json={
            "username": "test_first_login",
            "password": "TempPass123!"
        }
    )
    
    if user_login_response.status_code == 200:
        user_data = user_login_response.json()
        user_token = user_data['access']
        user_headers = {"Authorization": f"Bearer {user_token}"}
        print("✅ User login successful")
        print(f"   must_change_password: {user_data['user']['must_change_password']}")
        
        if user_data['user']['must_change_password']:
            print("   ⚠️  User must change password on first login")
        else:
            print("   ❌ Expected must_change_password to be True")
    else:
        print(f"❌ User login failed: {user_login_response.status_code}")
        return
    
    # 4. Try to access protected resource before changing password
    print("\n4. Trying to access protected resource...")
    me_response = requests.get(
        f"{BASE_URL}/me/",
        headers=user_headers
    )
    
    if me_response.status_code == 200:
        print("✅ Can access protected resource (expected)")
        print("   Note: Frontend should show password change modal")
    else:
        print(f"❌ Cannot access protected resource: {me_response.status_code}")
    
    # 5. Change password
    print("\n5. Changing password...")
    change_password_data = {
        "old_password": "TempPass123!",
        "new_password": "NewSecurePass123!",
        "new_password_confirm": "NewSecurePass123!"
    }
    
    change_response = requests.post(
        f"{BASE_URL}/change-password/",
        headers=user_headers,
        json=change_password_data
    )
    
    if change_response.status_code == 200:
        print("✅ Password changed successfully")
        print(f"   {change_response.json()['detail']}")
    else:
        print(f"❌ Failed to change password: {change_response.status_code}")
        print(change_response.json())
        return
    
    # 6. Login again with new password
    print("\n6. Logging in with new password...")
    new_login_response = requests.post(
        f"{BASE_URL}/login/",
        json={
            "username": "test_first_login",
            "password": "NewSecurePass123!"
        }
    )
    
    if new_login_response.status_code == 200:
        new_user_data = new_login_response.json()
        print("✅ Login with new password successful")
        print(f"   must_change_password: {new_user_data['user']['must_change_password']}")
        
        if not new_user_data['user']['must_change_password']:
            print("   ✅ must_change_password is now False")
        else:
            print("   ❌ Expected must_change_password to be False")
    else:
        print(f"❌ Login with new password failed: {new_login_response.status_code}")
    
    # 7. Cleanup - delete test user
    print("\n7. Cleaning up test user...")
    delete_response = requests.delete(
        f"{BASE_URL}/user-management/{new_user['id']}/",
        headers=admin_headers
    )
    
    if delete_response.status_code == 200:
        print("✅ Test user deleted")
    else:
        print(f"⚠️  Failed to delete test user: {delete_response.status_code}")
    
    print("\n" + "="*50)
    print("First Login Password Change Flow Test Completed!")
    print("="*50)


if __name__ == "__main__":
    test_first_login_flow()

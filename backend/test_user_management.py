"""
Test script for user management API endpoints.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/auth"

def test_user_management():
    """Test user management endpoints."""
    
    # 1. Login as admin
    print("1. Logging in as admin...")
    login_response = requests.post(
        f"{BASE_URL}/login/",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.json())
        return
    
    token = login_response.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")
    
    # 2. List all users
    print("\n2. Listing all users...")
    users_response = requests.get(
        f"{BASE_URL}/user-management/",
        headers=headers
    )
    
    if users_response.status_code == 200:
        response_data = users_response.json()
        # Handle paginated response
        if isinstance(response_data, dict) and 'results' in response_data:
            users = response_data['results']
        else:
            users = response_data
        
        print(f"✅ Found {len(users)} users")
        for user in users:
            print(f"   - {user['username']} ({user['role_name']}) - Active: {user['is_active']}")
    else:
        print(f"❌ Failed to list users: {users_response.status_code}")
        print(users_response.json())
    
    # 3. Create a new user
    print("\n3. Creating a new user...")
    new_user_data = {
        "username": "test_operator",
        "email": "test_operator@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "first_name": "Test",
        "last_name": "Operator",
        "role": 3  # OPERADOR role ID
    }
    
    create_response = requests.post(
        f"{BASE_URL}/user-management/",
        headers=headers,
        json=new_user_data
    )
    
    if create_response.status_code == 201:
        new_user = create_response.json()
        user_id = new_user['id']
        print(f"✅ User created: {new_user['username']} (ID: {user_id})")
    else:
        print(f"❌ Failed to create user: {create_response.status_code}")
        print(create_response.json())
        return
    
    # 4. Update user
    print("\n4. Updating user...")
    update_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "phone": "123-456-7890"
    }
    
    update_response = requests.patch(
        f"{BASE_URL}/user-management/{user_id}/",
        headers=headers,
        json=update_data
    )
    
    if update_response.status_code == 200:
        updated_user = update_response.json()
        print(f"✅ User updated: {updated_user['first_name']} {updated_user['last_name']}")
    else:
        print(f"❌ Failed to update user: {update_response.status_code}")
        print(update_response.json())
    
    # 5. Deactivate user
    print("\n5. Deactivating user...")
    deactivate_response = requests.post(
        f"{BASE_URL}/user-management/{user_id}/deactivate/",
        headers=headers
    )
    
    if deactivate_response.status_code == 200:
        deactivated_user = deactivate_response.json()
        print(f"✅ User deactivated: {deactivated_user['username']} - Active: {deactivated_user['is_active']}")
    else:
        print(f"❌ Failed to deactivate user: {deactivate_response.status_code}")
        print(deactivate_response.json())
    
    # 6. Activate user
    print("\n6. Activating user...")
    activate_response = requests.post(
        f"{BASE_URL}/user-management/{user_id}/activate/",
        headers=headers
    )
    
    if activate_response.status_code == 200:
        activated_user = activate_response.json()
        print(f"✅ User activated: {activated_user['username']} - Active: {activated_user['is_active']}")
    else:
        print(f"❌ Failed to activate user: {activate_response.status_code}")
        print(activate_response.json())
    
    # 7. Reset password
    print("\n7. Resetting user password...")
    reset_data = {
        "new_password": "NewPass123!",
        "new_password_confirm": "NewPass123!"
    }
    
    reset_response = requests.post(
        f"{BASE_URL}/user-management/{user_id}/reset_password/",
        headers=headers,
        json=reset_data
    )
    
    if reset_response.status_code == 200:
        print(f"✅ Password reset successful")
        print(f"   {reset_response.json()['detail']}")
    else:
        print(f"❌ Failed to reset password: {reset_response.status_code}")
        print(reset_response.json())
    
    # 8. Filter users by role
    print("\n8. Filtering users by role (OPERADOR)...")
    filter_response = requests.get(
        f"{BASE_URL}/user-management/?role=OPERADOR",
        headers=headers
    )
    
    if filter_response.status_code == 200:
        response_data = filter_response.json()
        filtered_users = response_data['results'] if isinstance(response_data, dict) and 'results' in response_data else response_data
        print(f"✅ Found {len(filtered_users)} OPERADOR users")
    else:
        print(f"❌ Failed to filter users: {filter_response.status_code}")
    
    # 9. Search users
    print("\n9. Searching users by name...")
    search_response = requests.get(
        f"{BASE_URL}/user-management/?search=Test",
        headers=headers
    )
    
    if search_response.status_code == 200:
        response_data = search_response.json()
        search_results = response_data['results'] if isinstance(response_data, dict) and 'results' in response_data else response_data
        print(f"✅ Found {len(search_results)} users matching 'Test'")
    else:
        print(f"❌ Failed to search users: {search_response.status_code}")
    
    # 10. Delete user (soft delete)
    print("\n10. Deleting user (soft delete)...")
    delete_response = requests.delete(
        f"{BASE_URL}/user-management/{user_id}/",
        headers=headers
    )
    
    if delete_response.status_code == 200:
        print(f"✅ User deleted (deactivated)")
        print(f"   {delete_response.json()['detail']}")
    else:
        print(f"❌ Failed to delete user: {delete_response.status_code}")
        print(delete_response.json())
    
    print("\n" + "="*50)
    print("User Management API Tests Completed!")
    print("="*50)


if __name__ == "__main__":
    test_user_management()

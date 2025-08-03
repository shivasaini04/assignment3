import requests
import json

BASE_URL = 'http://localhost:5009'

def test_home():
    print("\nTesting Home Endpoint:")
    response = requests.get(f"{BASE_URL}/")
    print(f"Response: {response.text}")

def test_create_user():
    print("\nTesting Create User:")
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Response: {response.text}")
    return response.json()['data']['id'] if response.status_code == 201 else None

def test_get_users():
    print("\nTesting Get All Users:")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Response: {response.text}")

def test_get_user(user_id):
    print(f"\nTesting Get User (ID: {user_id}):")
    response = requests.get(f"{BASE_URL}/user/{user_id}")
    print(f"Response: {response.text}")

def test_update_user(user_id):
    print(f"\nTesting Update User (ID: {user_id}):")
    update_data = {
        "name": "John Updated",
        "email": "john.updated@example.com"
    }
    response = requests.put(f"{BASE_URL}/user/{user_id}", json=update_data)
    print(f"Response: {response.text}")

def test_search_users():
    print("\nTesting Search Users:")
    response = requests.get(f"{BASE_URL}/search?name=John")
    print(f"Response: {response.text}")

def test_login():
    print("\nTesting Login:")
    login_data = {
        "email": "john.updated@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Response: {response.text}")

def run_all_tests():
    print("Starting API Tests...")
    
    # Test home endpoint
    test_home()
    
    # Test user creation and get the user ID
    user_id = test_create_user()
    
    if user_id:
        # Test other endpoints
        test_get_users()
        test_get_user(user_id)
        test_update_user(user_id)
        test_search_users()
        test_login()
    else:
        print("Failed to create user, skipping remaining tests.")

if __name__ == "__main__":
    run_all_tests()

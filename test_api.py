import pytest  # Import pytest for writing and running tests
import json  # Import json for handling JSON data
from app import app_API, User  # Import Flask app for testing

@pytest.fixture
def client():
    """Fixture to set up Flask test client for API testing"""
    app_API.config['TESTING'] = True  # Enable testing mode
    with app_API.test_client() as client:
        yield client  # Provide test client to test functions

def test_get_users_empty(client):
    """Test GET /users: Verify it returns an empty array when no users exist"""
    response = client.get('/users')  # Send GET request to /users
    assert response.status_code == 200  # Check for 200 OK status
    assert response.json == []  # Verify response is an empty array
    assert response.headers['Content-Type'] == 'application/json'  # Verify JSON content type

def test_create_user_success(client):
    """Test POST /users: Verify it creates a new user successfully"""
    user_data = {
        'name': 'John',
        'surname': 'Doe',
        'phone': '1234567890',
        'address': '123 Main St'
    }  # Sample user data
    response = client.post('/users', json=user_data)  # Send POST request
    assert response.status_code == 201  # Check for 201 Created status
    assert response.headers['Content-Type'] == 'application/json'  # Verify JSON content type
    # Verify all expected fields are in response
    assert all(key in response.json for key in ['id', 'name', 'surname', 'phone', 'address'])
    # Verify response data matches input
    assert response.json['name'] == user_data['name']
    assert response.json['surname'] == user_data['surname']
    assert response.json['phone'] == user_data['phone']
    assert response.json['address'] == user_data['address']

def test_create_user_missing_fields(client):
    """Test POST /users: Verify it rejects requests with missing fields"""
    user_data = {'name': 'John'}  # Incomplete user data
    response = client.post('/users', json=user_data)  # Send POST request
    assert response.status_code == 400  # Check for 400 Bad Request status
    assert response.json['error'] == 'Missing required fields'  # Verify error message

def test_get_user_success(client):
    """Test GET /users/{id}: Verify it returns correct user for valid ID"""
    # Create a user first
    user_data = {
        'name': 'Jane',
        'surname': 'Smith',
        'phone': '0987654321',
        'address': '456 Oak Ave'
    }
    create_response = client.post('/users', json=user_data)  # Send POST request
    user_id = create_response.json['id']  # Get created user's ID
    
    # Get the user by ID
    response = client.get(f'/users/{user_id}')  # Send GET request
    assert response.status_code == 200  # Check for 200 OK status
    assert response.json['id'] == user_id  # Verify correct user ID
    assert response.json['name'] == user_data['name']  # Verify user data

def test_get_user_not_found(client):
    """Test GET /users/{id}: Verify it returns 404 for invalid ID"""
    response = client.get('/users/invalid_id')  # Send GET request with invalid ID
    assert response.status_code == 404  # Check for 404 Not Found status
    assert response.json['error'] == 'User not found'  # Verify error message

def test_update_user_success(client):
    """Test PUT /users/{id}: Verify it updates user data successfully"""
    # Create a user first
    user_data = {
        'name': 'Bob',
        'surname': 'Johnson',
        'phone': '1112223333',
        'address': '789 Pine Rd'
    }
    create_response = client.post('/users', json=user_data)  # Send POST request
    user_id = create_response.json['id']  # Get created user's ID
    
    # Update user data
    update_data = {
        'name': 'Robert',
        'surname': 'Johnson',
        'phone': '4445556666',
        'address': '321 Cedar Ln'
    }
    response = client.put(f'/users/{user_id}', json=update_data)  # Send PUT request
    assert response.status_code == 200  # Check for 200 OK status
    # Verify updated fields
    assert response.json['name'] == update_data['name']
    assert response.json['phone'] == update_data['phone']
    assert response.json['address'] == update_data['address']

def test_delete_user_success(client):
    """Test DELETE /users/{id}: Verify it deletes user successfully"""
    # Create a user first
    user_data = {
        'name': 'Alice',
        'surname': 'Brown',
        'phone': '7778889999',
        'address': '654 Elm St'
    }
    create_response = client.post('/users', json=user_data)  # Send POST request
    user_id = create_response.json['id']  # Get created user's ID
    
    # Delete the user
    response = client.delete(f'/users/{user_id}')  # Send DELETE request
    assert response.status_code == 204  # Check for 204 No Content status
    assert response.data == b''  # Verify empty response body
    
    # Verify user is deleted
    response = client.get(f'/users/{user_id}')  # Send GET request
    assert response.status_code == 404  # Check for 404 Not Found status

def test_user_model():
    """Unit test for User model: Verify User object creation and serialization"""
    user = User(
        name='Test',
        surname='User',
        phone='1234567890',
        address='Test Address'
    )  # Create a User instance
    user_dict = user.to_dict()  # Convert to dictionary
    assert isinstance(user_dict['id'], str)  # Verify ID is a string
    assert user_dict['name'] == 'Test'  # Verify name
    assert user_dict['surname'] == 'User'  # Verify surname
    assert user_dict['phone'] == '1234567890'  # Verify phone
    assert user_dict['address'] == 'Test Address'  # Verify address
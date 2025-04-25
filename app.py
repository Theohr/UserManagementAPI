from flask import Flask, request, jsonify  # Import Flask for API, request for handling HTTP requests, jsonify for JSON responses
from http import HTTPStatus  # Import HTTP status codes for consistent response codes
import uuid  # Import uuid for generating unique user IDs

# Initialize Flask application
app_API = Flask(__name__)

# In-memory storage for users, using a dictionary with user IDs as keys
users = {}

# User class to represent a user object with required properties
class User:
    def __init__(self, name, surname, phone, address):
        """Initialize a User with name, surname, phone, and address; auto-generate a unique ID"""
        self.id = str(uuid.uuid4())  # Generate a unique ID using UUID4
        self.name = name  # User's first name
        self.surname = surname  # User's last name
        self.phone = phone  # User's phone number
        self.address = address  # User's address

    def to_dict(self):
        """Convert User object to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'phone': self.phone,
            'address': self.address
        }

@app_API.route('/users', methods=['GET'])
def get_users():
    """Handle GET /users: Return a list of all users as a JSON array"""
    # Convert each User object to a dictionary and return as JSON with 200 OK
    return jsonify([user.to_dict() for user in users.values()]), HTTPStatus.OK

@app_API.route('/users', methods=['POST'])
def create_user():
    """Handle POST /users: Create a new user from JSON payload"""
    data = request.get_json()  # Get JSON data from request body
    # Validate that all required fields are present
    if not all(key in data for key in ['name', 'surname', 'phone', 'address']):
        return jsonify({'error': 'Missing required fields'}), HTTPStatus.BAD_REQUEST
    
    # Create a new User instance with provided data
    user = User(
        name=data['name'],
        surname=data['surname'],
        phone=data['phone'],
        address=data['address']
    )
    users[user.id] = user  # Store user in in-memory dictionary
    # Return created user as JSON with 201 Created
    return jsonify(user.to_dict()), HTTPStatus.CREATED

@app_API.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Handle GET /users/{id}: Retrieve a user by their ID"""
    user = users.get(user_id)  # Look up user by ID in dictionary
    if not user:
        # Return 404 Not Found if user doesn't exist
        return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND
    # Return user as JSON with 200 OK
    return jsonify(user.to_dict()), HTTPStatus.OK

@app_API.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Handle PUT /users/{id}: Update an existing user's data"""
    user = users.get(user_id)  # Look up user by ID
    if not user:
        # Return 404 Not Found if user doesn't exist
        return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND
    
    data = request.get_json()  # Get JSON data from request body
    # Update user fields with new values, keeping existing values if not provided
    user.name = data.get('name', user.name)
    user.surname = data.get('surname', user.surname)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)
    # Return updated user as JSON with 200 OK
    return jsonify(user.to_dict()), HTTPStatus.OK

@app_API.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Handle DELETE /users/{id}: Delete a user by their ID"""
    if user_id not in users:
        # Return 404 Not Found if user doesn't exist
        return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND
    del users[user_id]  # Remove user from dictionary
    # Return empty response with 204 No Content
    return '', HTTPStatus.NO_CONTENT

if __name__ == '__main__':
    """Run the Flask application in debug mode if executed directly"""
    app_API.run(debug=True)
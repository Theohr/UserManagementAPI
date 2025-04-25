# User Management API

## Overview
This is a simple RESTful User Management API built with Flask and tested with pytest. The API stores data in memory and provides endpoints for CRUD operations on user objects.

## Prerequisites
- Python 3.8+
- pip package manager

## Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install flask pytest pytest-flask
   ```
4. Run the API:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

## Running Tests
1. Ensure you're in the project directory with the virtual environment activated
2. Run tests with:
   ```bash
   pytest test_api.py -v
   ```

## API Endpoints
- GET /users - List all users
- POST /users - Create a new user
- GET /users/{id} - Get a specific user
- PUT /users/{id} - Update a user
- DELETE /users/{id} - Delete a user

## User Model
```json
{
    "id": "string",
    "name": "string",
    "surname": "string",
    "phone": "string",
    "address": "string"
}
```

## Testing
The test suite includes:
- API integration tests for all endpoints
- Status code verification
- Response body validation
- Content-Type header checks
- Error case handling
- Unit test for User model

## Manual Testing
You can use Postman or curl to manually test the API. Example curl command:
```bash
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name":"John","surname":"Doe","phone":"1234567890","address":"123 Main St"}'
```

## Notes
- The API uses in-memory storage, so data is reset when the server restarts
- UUIDs are used for user IDs
- Comprehensive error handling is implemented
- Tests are organized in a separate test file with clear naming conventions

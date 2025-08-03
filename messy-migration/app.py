from flask import Flask, request, jsonify
import sqlite3
import json
from app.models.user import User
from app.models.user_repository import UserRepository
from app.utils.response import success_response, error_response

app = Flask(__name__)

@app.route('/')
def home():
    return success_response(message="User Management System")

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = UserRepository.get_all_users()
        return success_response(data=users)
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = UserRepository.get_user_by_id(user_id)
        if user:
            return success_response(data=user)
        return error_response("User not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        user = User(
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password')
        )

        validation_errors = user.validate()
        if validation_errors:
            return error_response(validation_errors[0], 400)

        user_id = UserRepository.create_user(user)
        return success_response(
            data={'id': user_id},
            message="User created successfully",
            status_code=201
        )
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return error_response("Name and email are required", 400)

        if UserRepository.update_user(user_id, name, email):
            return success_response(message="User updated successfully")
        return error_response("User not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        if UserRepository.delete_user(user_id):
            return success_response(message="User deleted successfully")
        return error_response("User not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/search', methods=['GET'])
def search_users():
    try:
        name = request.args.get('name')
        if not name:
            return error_response("Name parameter is required", 400)

        users = UserRepository.search_users_by_name(name)
        return success_response(data=users)
    except Exception as e:
        return error_response(str(e), 500)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return error_response("Email and password are required", 400)

        user = UserRepository.get_user_by_credentials(email, password)
        if user:
            return success_response(data=user, message="Login successful")
        return error_response("Invalid credentials", 401)
    except Exception as e:
        return error_response(str(e), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
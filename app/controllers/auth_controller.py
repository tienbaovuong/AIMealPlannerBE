# app/controller/auth_controller.py

from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService  # Import your AuthService

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    token = AuthService.login(email, password)
    if token:
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# app/routes.py

from flask import Blueprint, request, jsonify
from app.services import AuthService  # Assuming you have an AuthService for business logic

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    token = AuthService.login(email, password)
    if token:
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

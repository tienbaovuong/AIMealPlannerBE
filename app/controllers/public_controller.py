from flask import Blueprint, request, jsonify
from app.services.public_service import PublicService
import os

user_blueprint = Blueprint('public', __name__)

@user_blueprint.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    weight = request.form.get('weight')
    height = request.form.get('height')
    age = request.form.get('age')
    gender = request.form.get('gender')

    # Parse allergies and dietary preferences
    allergies_str = request.form.get('allergies')  # Get the comma-separated string
    dietaryPreferences_str = request.form.get('dietaryPreferences')  # Get the comma-separated string

    allergies = [a.strip() for a in allergies_str.split(',')] if allergies_str else []
    dietaryPreferences = [d.strip() for d in dietaryPreferences_str.split(',')] if dietaryPreferences_str else []

    upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    profile_picture = request.files.get('profilePicture')
    user_data = {
        'email': email,
        'name': name,
        'password': password,  # Hash this before saving in production
        'weight': float(weight) if weight else 0.0,
        'height': float(height) if height else 0.0,
        'age': int(age) if age else 0,
        'gender': gender or '',
        'allergies': allergies if allergies else [],  # Store as empty list if no allergies
        'dietaryPreferences': dietaryPreferences if dietaryPreferences else [],  # Store as empty list if no preferences
        'profile_picture': ''  # Default to empty string; it will be updated later
    }
    response, status_code = PublicService.create_user(user_data, profile_picture)

    return jsonify(response), status_code


    # data = request.json
    # email = data.get('email')
    # username = data.get('username')
    # password = data.get('password')
    # response, status_code = PublicService.create_user(email, username, password)


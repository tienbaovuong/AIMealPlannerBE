from flask import Blueprint, request, jsonify
from app.middleware.auth_middleware import token_required
from app.services.user_service import UserService
from werkzeug.utils import secure_filename
import os
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/edit_profile', methods=['PUT'])
@token_required
def edit_profile(current_user_id):
    update_data = request.form
    if not update_data:
        return jsonify({'message': 'No data provided!'}), 400

    # Create a dictionary for updated data, excluding email and password
    profile_data = {
        'name': update_data.get('name', ''),
        'weight': float(update_data.get('weight', 0.0)),  # Ensure float
        'height': float(update_data.get('height', 0.0)),  # Ensure float
        'age': int(update_data.get('age', 0)),            # Ensure int
        'gender': update_data.get('gender', ''),
        'allergies': update_data.getlist('allergies'),    # Handle as a list
        'dietaryPreferences': update_data.getlist('dietaryPreferences'),  # Handle as a list
        'profile_picture': ''  # Placeholder for profile picture
    }

    profile_picture = request.files.get('profilePicture')
    if profile_picture:
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)  # Create uploads directory if it doesn't exist

        filename = secure_filename(profile_picture.filename)
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{current_user_id}_{timestamp}_{filename}"
        profile_picture_path = os.path.join(upload_folder, new_filename)

        try:
            profile_picture.save(profile_picture_path)
            profile_data['profile_picture'] = profile_picture_path  # Update the profile picture path
        except Exception as e:
            return jsonify({'error': f'Error saving profile picture: {str(e)}'}), 500

    # Remove email and password from the update data (if they were passed)
    profile_data.pop('email', None)
    profile_data.pop('password', None)

    # Validate types and check for changes
    expected_types = {
        'name': str,
        'weight': float,
        'height': float,
        'age': int,
        'gender': str,
        'allergies': list,
        'dietaryPreferences': list,
        'profile_picture': (str, type(None))  # Can be a string or None
    }

    for key, expected_type in expected_types.items():
        value = profile_data.get(key)
        if not isinstance(value, expected_type) and value is not None:
            return jsonify({'message': f'Invalid type for {key}: expected {expected_type.__name__}'}), 400

    success = UserService.update_user(current_user_id, profile_data)
    if success:
        return jsonify({'message': 'Profile updated successfully!'}), 200
    else:
        return jsonify({'message': 'Failed to update profile!', 'user_id': current_user_id, 'update_data': profile_data}), 400

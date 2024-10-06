# app/services/user_service.py

import os
from werkzeug.security import generate_password_hash
from app.db.mongo import mongo
from werkzeug.utils import secure_filename
from datetime import datetime

class PublicService:

    @staticmethod
    def create_user(user_data, profile_picture):
        try:
            email = user_data.get('email')
            hashed_password = generate_password_hash(user_data.get('password'))
            user_data['password'] = hashed_password

            # Check for existing email
            if mongo.db.users.find_one({'email': email}):
                return {'error': 'Email already exists'}, 400

            # Insert user data into MongoDB
            result = mongo.db.users.insert_one(user_data)
            user_id = str(result.inserted_id)  # Get the inserted document's _id

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # Save profile picture with the new filename
            if profile_picture is not None:
                filename = secure_filename(profile_picture.filename)
                # Append the user ID to the filename
                new_filename = f"{user_id}_{timestamp}_{filename}"
                picture_path = os.path.join('uploads', new_filename)  # Ensure this directory exists
                profile_picture.save(picture_path)

                # Update the user document with the new profile picture path
                mongo.db.users.update_one(
                    {'_id': result.inserted_id},
                    {'$set': {'profile_picture': picture_path}}
                )

            # Return success response
            return {'message': 'User created successfully', 'user_id': user_id}, 201
        except Exception as e:
            # Return error response
            return {'error': str(e)}, 500
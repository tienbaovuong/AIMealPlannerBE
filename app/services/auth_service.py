# app/services/auth_service.py

import jwt
import datetime
from werkzeug.security import check_password_hash
from app.db.mongo import mongo  # Import the mongo instance

SECRET_KEY = 'npwedhrjskt32oerka9'  # Change this to a secure key

class AuthService:
    @staticmethod
    def login(email, password):
        user = mongo.db.users.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            token = jwt.encode({
                'user_id': str(user['_id']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Set token expiration time
            }, SECRET_KEY, algorithm='HS256')
            return token
        return None

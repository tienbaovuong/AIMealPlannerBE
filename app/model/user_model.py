from app.db.mongo import mongo

def get_user_by_id(user_id):
    user = mongo.db.users.find_one({'_id': user_id})  # Assuming user_id is an ObjectId
    return user  # Return user data as a dictionary

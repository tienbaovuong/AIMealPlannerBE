# from app.db.mongo import mongo
# from bson.objectid import ObjectId

# class UserService:
#     @staticmethod
#     def update_user(user_id, update_data):
#         # Ensure user_id is an ObjectId
#         try:
#             user_id = ObjectId(user_id)
#         except Exception as e:
#             return False  # Invalid user_id format

#         result = mongo.db.users.update_one({"_id": user_id}, {"$set": update_data})
#         return result.modified_count > 0

from app.db.mongo import mongo
from bson.objectid import ObjectId

class UserService:
    @staticmethod
    def update_user(user_id, update_data):
        # Ensure user_id is an ObjectId
        try:
            user_id = ObjectId(user_id)
        except Exception as e:
            return False  # Invalid user_id format

        result = mongo.db.users.update_one({"_id": user_id}, {"$set": update_data})
        return result.modified_count > 0

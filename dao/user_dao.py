from datetime import datetime
from bson import ObjectId

class UserDAO:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, username, password_hash):
        self.collection.insert_one({
            "username": username,
            "password_hash": password_hash,
            "created_at": datetime.utcnow()
        })

    def get_by_username(self,username):
        return self.collection.find_one({"username": username})
    
    def get_by_id(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})
    
    def update_username(self, user_id, new_username):
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"username": new_username}}
        )
    
    def update_password(self, user_id, new_password_hash):
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password_hash": new_password_hash}}
        )
        
    def update_avatar(self, user_id, avatar):
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"avatar": avatar}}
        )
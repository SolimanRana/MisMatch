from datetime import datetime

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
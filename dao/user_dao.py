from datetime import datetime
from bson import ObjectId

#requirements
#m3:create accound and login
#c4:change useername and pw
#c5:choose avatar from the given emojis

class UserDAO:
    #initialize DAO with db connection
    def __init__(self, db):
        #set collection reference to users collection
        self.collection = db.users

    #create a new user account in the db
    def create_user(self, username, password_hash):
        #insert new user doc with username, hashed pw and timestamp
        self.collection.insert_one({
            "username": username,
            "password_hash": password_hash,
            "created_at": datetime.utcnow()
        })

    #get user by username for login
    def get_by_username(self,username):
        #find and return user doc by username
        return self.collection.find_one({"username": username})

    #helper function to get user by their ID
    def get_by_id(self, user_id):
        #find and return user doc by objectID
        return self.collection.find_one({"_id": ObjectId(user_id)})

    #update usernaame in the db
    def update_username(self, user_id, new_username):
        #update username field for specified user
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"username": new_username}}
        )
    #update pw in the db
    def update_password(self, user_id, new_password_hash):
        #update password_hash field for specified user
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password_hash": new_password_hash}}
        )

    #update avatar emoji in the db
    def update_avatar(self, user_id, avatar):
        #update avatar field for specified user
        self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"avatar": avatar}}
        )
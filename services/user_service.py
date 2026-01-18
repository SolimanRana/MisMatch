from argon2 import PasswordHasher
from dao.user_dao import UserDAO
from argon2.exceptions import VerifyMismatchError

#requirements
#m3:create account and login
#c4: change username and pw
#c5:choose avatar from given option


#create pwhasher instance
ph = PasswordHasher()

class UserService:
    #initalize service with db connection
    def __init__(self, db):
        #create userdao instance for db operations
        self.user_dao = UserDAO(db)

    #register a new user account
    def register_user(self, username, password):
    #does name exist?
        if self.user_dao.get_by_username(username):
            raise ValueError("Username already exists")
        #hash pw usig Argon2
        password_hash = ph.hash(password)
        #create new user in db
        self.user_dao.create_user(username, password_hash)

    #return cretaed user doc
        return self.user_dao.get_by_username(username)

    #authenticate user for login
    def authenticate_user(self, username, password):
        #get user from db
        user = self.user_dao.get_by_username(username)

        #return error if user not found
        if not user:
            raise ValueError("Invalid username or password")

        #verify pw against stored hash
        try:
            ph.verify(user["password_hash"], password)
        except VerifyMismatchError:
            #return error if pw doesn't match
            raise ValueError("Invalid username or password")

        #return user doc if authentication works
        return user

    #change username
    def change_username(self, user_id, new_username):
        #check if new username already exists
        if self.user_dao.get_by_username(new_username):
            raise ValueError("username already exists")

        #update username in the db
        self.user_dao.update_username(user_id, new_username)
     #change pw
    def change_password(self, user_id, old_password, new_password):
        #get current pw
        user = self.user_dao.get_by_id(user_id)

        #verify old pw is correct
        try:
            ph.verify(user["password_hash"], old_password)
        except VerifyMismatchError:
            #return error if old pw doesnt match
            raise ValueError("Old Password is incorrect")

        #hash new pw
        new_hash = ph.hash(new_password)
        #update pw in the db
        self.user_dao.update_password(user_id, new_hash)
        
    def change_avatar(self, user_id, avatar):
        #update avatar in db
        self.user_dao.update_avatar(user_id, avatar)
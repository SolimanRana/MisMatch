from argon2 import PasswordHasher
from dao.user_dao import UserDAO
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

class UserService:
    def __init__(self, db):
        self.user_dao = UserDAO(db)

    def register_user(self, username, password):

        if self.user_dao.get_by_username(username):
            raise ValueError("Username already exists")

        password_hash = ph.hash(password)
        self.user_dao.create_user(username, password_hash)

        return self.user_dao.get_by_username(username)

    def authenticate_user(self, username, password):
        user = self.user_dao.get_by_username(username)

        if not user:
            raise ValueError("Invalid username or password")
        
        try:
            ph.verify(user["password_hash"], password)
        except VerifyMismatchError:
            raise ValueError("Invalid username or password")

        return user
    
    def change_username(self, user_id, new_username):
        if self.user_dao.get_by_username(new_username):
            raise ValueError("username already exists")
        
        self.user_dao.update_username(user_id, new_username)
        
    def change_password(self, user_id, old_password, new_password):
        user = self.user_dao.get_by_id(user_id)
        
        try:
            ph.verify(user["password_hash"], old_password)
        except VerifyMismatchError:
            raise ValueError("Old Password is incorrect")
        
        new_hash = ph.hash(new_password)
        self.user_dao.update_password(user_id, new_hash)
        
    def change_avatar(self, user_id, avatar):
        self.user_dao.update_avatar(user_id, avatar)
from models.base_model import BaseModel
from flask_login import UserMixin
import peewee as pw
import re
from werkzeug.security import generate_password_hash

class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    hash_password = pw.CharField(null=False)
    password = None
    confirm_password = None
    profile_image_url = pw.CharField(null=True)

    def validate(self):
        existing_user_username = User.get_or_none(User.username ** self.username)
        if existing_user_username and existing_user_username.id != self.id:
            self.errors.append(f"{self.username} already taken!")
        
        existing_user_email = User.get_or_none(User.email ** self.email)
        if existing_user_email and existing_user_email.id != self.id:
            self.errors.append(f"{self.email} already taken!")
        
        if (len(self.username) < 6 or len(self.username) > 50) or "@" in self.username:
            self.errors.append("Username needs to be 6-50 characters long and can't contain @.")
        
        if len(self.name) == 0 or len(self.name) > 50:
            self.errors.append("Name needs to be 1-50 characters long.")

        validate_email = self.email.split("@")
        if len(validate_email[0]) < 4 and len(validate_email[0]) > 20:
            self.errors.append("Email needs to be between 4-20 characters long.")

        if self.password and self.confirm_password:
            if len(self.password) < 8 and len(self.password) > 20:
                self.errors.append("Password needs to be 8-20 characters and have uppercase, lowercase, and special characters.")

            if self.password != self.confirm_password:
                self.errors.append("Passwords do not match!")

            has_lower = re.search(r"[a-z]", self.password)
            has_upper = re.search(r"[A-Z]", self.password)
            has_special = re.search(r"[^a-zA-Z0-9]", self.password)
            if has_lower and has_upper and has_special:
                self.hash_password = generate_password_hash(self.password)
            else:
                self.errors.append("Password needs to have at least 1 uppercase letter, 1 lower case letter, and 1 special character.")



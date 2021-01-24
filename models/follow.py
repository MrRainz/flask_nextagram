from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Follow(BaseModel):
    follower = pw.ForeignKeyField(User, backref="followings")
    following = pw.ForeignKeyField(User, backref="followers")
    approved = pw.BooleanField(default=False)
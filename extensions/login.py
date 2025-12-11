from flask_login import LoginManager
from auth.models import User
from extensions.mongo import mongo
from bson.objectid import ObjectId

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)  # ✅ ensures User has is_admin
    return None

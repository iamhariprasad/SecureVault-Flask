import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/securevault")
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "encrypted_files")
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

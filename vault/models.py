from extensions.mongo import mongo
from bson import ObjectId

def add_file_record(user_id, original_filename, encrypted_filename, salt, iv):
    mongo.db.files.insert_one({
        "user_id": ObjectId(user_id),
        "original_filename": original_filename,
        "encrypted_filename": encrypted_filename,
        "salt": salt,
        "iv": iv
    })


def get_user_files(user_id):
    return mongo.db.files.find({"user_id": ObjectId(user_id)})


def get_file_by_id(file_id):
    return mongo.db.files.find_one({"_id": ObjectId(file_id)})

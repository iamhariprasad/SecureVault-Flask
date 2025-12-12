from extensions.mongo import mongo
from bson import ObjectId
from datetime import datetime
import os, json, base64
from config import Config

def add_file_record(user_id, original_filename, encrypted_filename, salt, iv, file_size):
    mongo.db.files.insert_one({
        "user_id": ObjectId(user_id),
        "original_filename": original_filename,
        "encrypted_filename": encrypted_filename,
        "salt": salt,
        "iv": iv,
        "file_size": file_size,
        "uploaded_at": datetime.utcnow()
    })
    # Persist metadata (salt, iv) alongside the encrypted file for redundancy
    try:
        meta = {
            "original_name": original_filename,
            "salt": base64.b64encode(salt).decode("ascii"),
            "iv": base64.b64encode(iv).decode("ascii")
        }
        meta_path = os.path.join(Config.UPLOAD_FOLDER, encrypted_filename + ".meta.json")
        with open(meta_path, "w", encoding="utf-8") as mf:
            json.dump(meta, mf)
    except Exception:
        pass


def get_user_files(user_id):
    return mongo.db.files.find({"user_id": ObjectId(user_id)}).sort("uploaded_at", -1)


def get_file_by_id(file_id):
    return mongo.db.files.find_one({"_id": ObjectId(file_id)})


def delete_file_record(file_id, user_id):
    """Delete file record if it belongs to the user and remove metadata file."""
    # Fetch record to get filename for metadata cleanup
    record = mongo.db.files.find_one({
        "_id": ObjectId(file_id),
        "user_id": ObjectId(user_id)
    })
    result = mongo.db.files.delete_one({
        "_id": ObjectId(file_id),
        "user_id": ObjectId(user_id)
    })
    if result.deleted_count > 0 and record and record.get("encrypted_filename"):
        try:
            meta_path = os.path.join(Config.UPLOAD_FOLDER, record["encrypted_filename"] + ".meta.json")
            if os.path.exists(meta_path):
                os.remove(meta_path)
        except Exception:
            pass
        return True
    return False


def get_user_stats(user_id):
    """Get user file statistics"""
    files = list(mongo.db.files.find({"user_id": ObjectId(user_id)}))
    total_files = len(files)
    # Safely sum file sizes, handling non-numeric values
    total_size = 0
    for f in files:
        file_size = f.get("file_size", 0)
        try:
            total_size += float(file_size) if file_size else 0
        except (ValueError, TypeError):
            # Skip invalid file_size values
            pass
    return {
        "total_files": total_files,
        "total_size": int(total_size)
    }

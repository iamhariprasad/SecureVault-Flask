import os
from config import Config

STORAGE_DIR = os.environ.get("UPLOAD_FOLDER", "encrypted_files")
os.makedirs(STORAGE_DIR, exist_ok=True)


def save_encrypted_file(original_name, encrypted_data):
    """Save encrypted bytes and return ONLY the filename (string)."""
    
    encrypted_filename = original_name + ".enc"
    encrypted_path = os.path.join(STORAGE_DIR, encrypted_filename)

    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    # MUST return only filename (string)
    return encrypted_filename


def load_encrypted_file(encrypted_filename):
    """Load encrypted file and return bytes."""
    
    encrypted_path = os.path.join(STORAGE_DIR, encrypted_filename)

    if not os.path.exists(encrypted_path):
        print("ERROR: File NOT FOUND →", encrypted_path)
        return None

    with open(encrypted_path, "rb") as f:
        return f.read()


def delete_encrypted_file(encrypted_filename):
    """Delete encrypted file from disk."""
    encrypted_path = os.path.join(STORAGE_DIR, encrypted_filename)
    if os.path.exists(encrypted_path):
        os.remove(encrypted_path)
        return True
    return False
import os

STORAGE_DIR = "encrypted_files"

# Create directory if missing
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)


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

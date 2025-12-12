from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from extensions.mongo import mongo
from auth.utils import verify_password
from vault.encryption import encrypt_file, decrypt_file
from vault.storage import save_encrypted_file, load_encrypted_file
from vault.models import add_file_record, get_file_by_id
from bson.objectid import ObjectId

vault_api_bp = Blueprint("vault_api", __name__)

@vault_api_bp.route("/upload", methods=["POST"])
@jwt_required()
def api_upload():
    username = request.json.get("username")
    password = request.json.get("password")
    file_content = request.json.get("file_content")  # base64 encoded

    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "Invalid user"}), 400

    encrypted, salt, iv = encrypt_file(password, file_content.encode())
    encrypted_filename = save_encrypted_file(username + "_api_upload", encrypted)

    add_file_record(user["_id"], "api_file", encrypted_filename, salt, iv)

    return jsonify({"message": "File uploaded successfully"})


@vault_api_bp.route("/files/<file_id>", methods=["GET"])
@jwt_required()
def api_download(file_id):
    record = get_file_by_id(file_id)
    if not record:
        return jsonify({"error": "File not found"}), 404

    encrypted_data = load_encrypted_file(record["encrypted_filename"])

    password = request.args.get("password")
    decrypted = decrypt_file(password, record["salt"], record["iv"], encrypted_data)

    return jsonify({"file": decrypted.decode()})

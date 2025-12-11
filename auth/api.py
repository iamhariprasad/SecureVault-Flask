from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions.mongo import mongo
from auth.utils import verify_password
from flask import redirect, url_for


auth_api_bp = Blueprint("auth_api", __name__)

def home():
    return redirect(url_for("auth.login"))


@auth_api_bp.route("/login", methods=["POST"])
def api_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not verify_password(user["password_hash"], password):
        return jsonify({"error": "Invalid password"}), 401

    token = create_access_token(identity=str(user["_id"]))
    return jsonify({"token": token})

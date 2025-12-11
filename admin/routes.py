from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from bson import ObjectId
from io import BytesIO

from extensions.mongo import mongo
from vault.storage import load_encrypted_file
from vault.encryption import decrypt_file

# ---------------- BLUEPRINT ---------------- #
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ---------------- ADMIN CHECK ---------------- #
def admin_only():
    """
    Ensures only admins can access admin routes.
    """
    return (
        current_user.is_authenticated
        and bool(getattr(current_user, "is_admin", False))
    )


# ---------------- ADMIN DASHBOARD ---------------- #
@admin_bp.route("/dashboard")
@login_required
def admin_home():
    # block non-admins
    if not admin_only():
        flash("Admins only!", "danger")
        return redirect(url_for("auth.admin_login"))

    # Load all users and all files
    users = list(mongo.db.users.find())
    files = list(mongo.db.files.find())

    return render_template("admin_dashboard.html", users=users, files=files)


# ---------------- ADMIN DOWNLOAD USER FILE ---------------- #
@admin_bp.route("/download/<file_id>", methods=["POST"])
@login_required
def download_user_file(file_id):

    # ---- Admin permission check ----
    if not admin_only():
        flash("Unauthorized access!", "danger")
        return redirect(url_for("auth.admin_login"))

    # ---- Get password from form ----
    password = request.form.get("password")

    if not password:
        flash("Please enter the password to decrypt!", "danger")
        return redirect(url_for("admin.admin_home"))

    # ---- Fetch file metadata ----
    record = mongo.db.files.find_one({"_id": ObjectId(file_id)})

    if not record:
        flash("File not found!", "danger")
        return redirect(url_for("admin.admin_home"))

    # ---- Load encrypted file ----
    encrypted_data = load_encrypted_file(record["encrypted_filename"])

    if encrypted_data is None:
        flash("Encrypted file is missing on the server!", "danger")
        return redirect(url_for("admin.admin_home"))

    # ---- Attempt decryption ----
    try:
        decrypted = decrypt_file(
            password,
            record["salt"],
            record["iv"],
            encrypted_data
        )
    except Exception as e:
        print("Admin decrypt error:", e)
        flash("Wrong password — decryption failed!", "danger")
        return redirect(url_for("admin.admin_home"))

    # ---- Return decrypted file ----
    return send_file(
        BytesIO(decrypted),
        download_name=record["original_filename"],
        as_attachment=True
    )

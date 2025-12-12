from flask import Blueprint, render_template, request, redirect, send_file, flash, url_for, jsonify
from flask_login import login_required, current_user
from vault.encryption import encrypt_file, decrypt_file
from vault.storage import save_encrypted_file, load_encrypted_file, delete_encrypted_file
from vault.models import add_file_record, get_user_files, get_file_by_id, delete_file_record, get_user_stats
from io import BytesIO
from bson import ObjectId
import os

vault_bp = Blueprint("vault", __name__)


# ---------------- USER DASHBOARD ---------------- #
@vault_bp.route("/dashboard")
@login_required
def dashboard():
    files = list(get_user_files(current_user.id))
    stats = get_user_stats(current_user.id)
    return render_template("dashboard.html", files=files, stats=stats)



# ---------------- USER UPLOAD ---------------- #
@vault_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        password = request.form.get("password")

        if not file or not password:
            flash("Please provide a file and password.", "danger")
            return redirect(url_for("vault.upload"))

        data = file.read()
        file_size = len(data)
        encrypted_data, salt, iv = encrypt_file(password, data)

        encrypted_filename = save_encrypted_file(file.filename, encrypted_data)

        add_file_record(
            current_user.id,
            file.filename,
            encrypted_filename,
            salt,
            iv,
            file_size
        )

        flash("File uploaded successfully!", "success")
        return redirect(url_for("vault.dashboard"))

    return render_template("upload.html")


# ---------------- USER DOWNLOAD (GET) ---------------- #
@vault_bp.route("/download/<file_id>", methods=["GET"])
@login_required
def download(file_id):

    record = get_file_by_id(file_id)

    # Block access to another user's files
    if not record or str(record["user_id"]) != current_user.id:
        flash("Unauthorized file access!", "danger")
        return redirect(url_for("vault.dashboard"))

    password = request.args.get("password")

    if not password:
        flash("Please enter password to decrypt the file!", "danger")
        return redirect(url_for("vault.dashboard"))

    encrypted_data = load_encrypted_file(record["encrypted_filename"])

    if encrypted_data is None:
        flash("Encrypted file missing from server!", "danger")
        return redirect(url_for("vault.dashboard"))

    try:
        decrypted = decrypt_file(password, record["salt"], record["iv"], encrypted_data)
    except:
        flash("Incorrect password!", "danger")
        return redirect(url_for("vault.dashboard"))

    return send_file(
        BytesIO(decrypted),
        download_name=record["original_filename"],
        as_attachment=True
    )


# ---------------- DELETE FILE ---------------- #
@vault_bp.route("/delete/<file_id>", methods=["POST"])
@login_required
def delete_file(file_id):
    record = get_file_by_id(file_id)
    
    # Block access to another user's files
    if not record or str(record["user_id"]) != current_user.id:
        flash("Unauthorized file access!", "danger")
        return redirect(url_for("vault.dashboard"))
    
    # Delete encrypted file from disk
    delete_encrypted_file(record["encrypted_filename"])
    
    # Delete record from database
    if delete_file_record(file_id, current_user.id):
        flash("File deleted successfully!", "success")
    else:
        flash("Failed to delete file!", "danger")
    
    return redirect(url_for("vault.dashboard"))

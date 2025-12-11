from flask import Blueprint, render_template, redirect, url_for, flash
from auth.forms import RegisterForm, LoginForm
from auth.utils import hash_password, verify_password
from flask_login import login_user, logout_user
from extensions.mongo import mongo
from auth.models import User

auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER ---------------- #
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        users = mongo.db.users
        
        if users.find_one({"username": form.username.data}):
            flash("Username already exists!", "danger")
            return redirect(url_for("auth.register"))

        users.insert_one({
            "username": form.username.data,
            "password_hash": hash_password(form.password.data),
            "is_admin": False  # normal user
        })

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

# ---------------- USER LOGIN ---------------- #
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = mongo.db.users
        user = users.find_one({"username": form.username.data})

        if user and verify_password(user["password_hash"], form.password.data):
            
            # Login the user object
            login_user(User(user))

            # NORMAL LOGIN → always go to user dashboard
            return redirect(url_for("vault.dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html", form=form)


# ---------------- ADMIN LOGIN PAGE ---------------- #
@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = LoginForm()

    if form.validate_on_submit():
        users = mongo.db.users
        user = users.find_one({"username": form.username.data})

        if not user:
            flash("Admin not found!", "danger")
            return redirect(url_for("auth.admin_login"))

        if not user.get("is_admin", False):
            flash("Not an admin!", "danger")
            return redirect(url_for("auth.admin_login"))

        if not verify_password(user["password_hash"], form.password.data):
            flash("Wrong password!", "danger")
            return redirect(url_for("auth.admin_login"))

        # SUCCESS: login admin
        login_user(User(user))
        return redirect(url_for("admin.admin_home"))

    return render_template("admin_login.html", form=form)

# ---------------- LOGOUT ---------------- #
@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

from flask import Blueprint, render_template, redirect, url_for, flash, request
from auth.forms import RegisterForm, LoginForm
from auth.utils import hash_password, verify_password
from flask_login import login_user, logout_user
from extensions.mongo import mongo
from auth.models import User

auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER ---------------- #
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # #region agent log
    import json, os, time
    _log_path = os.path.join(os.path.dirname(__file__), '..', '.cursor', 'debug.log')
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"auth/routes.py:register","message":"register route called","data":{"method":request.method},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
    except: pass
    # #endregion
    
    form = RegisterForm()
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"auth/routes.py:register","message":"RegisterForm created","data":{"form_data":bool(request.form),"has_csrf_token":"csrf_token" in request.form},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
    except: pass
    # #endregion
    
    if form.validate_on_submit():
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"auth/routes.py:register","message":"Form validated successfully","data":{"username":form.username.data},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
        except: pass
        # #endregion
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
    else:
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"auth/routes.py:register","message":"Form validation failed or GET request","data":{"errors":form.errors if hasattr(form,'errors') else {},"method":request.method},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
        except: pass
        # #endregion

    return render_template("register.html", form=form)

# ---------------- USER LOGIN ---------------- #
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # #region agent log
    import json, os, time
    _log_path = os.path.join(os.path.dirname(__file__), '..', '.cursor', 'debug.log')
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"auth/routes.py:login","message":"login route called","data":{"method":request.method},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
    except: pass
    # #endregion
    
    form = LoginForm()
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"auth/routes.py:login","message":"LoginForm created","data":{"form_data":bool(request.form)},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
    except: pass
    # #endregion
    
    if form.validate_on_submit():
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"auth/routes.py:login","message":"Form validated successfully","data":{"username":form.username.data},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
        except: pass
        # #endregion
        
        users = mongo.db.users
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"auth/routes.py:login","message":"Attempting database query","data":{"username":form.username.data,"collection_exists":hasattr(mongo,'db')},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"G"})+"\n")
        except: pass
        # #endregion
        try:
            user = users.find_one({"username": form.username.data})
            # #region agent log
            try:
                with open(_log_path, 'a') as f:
                    f.write(json.dumps({"location":"auth/routes.py:login","message":"Database query result","data":{"user_found":user is not None},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"G"})+"\n")
            except: pass
            # #endregion
        except Exception as db_err:
            # #region agent log
            try:
                with open(_log_path, 'a') as f:
                    f.write(json.dumps({"location":"auth/routes.py:login","message":"Database query failed","data":{"error":str(db_err),"error_type":type(db_err).__name__},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"G"})+"\n")
            except: pass
            # #endregion
            flash("Database connection error. Please try again later.", "danger")
            return render_template("login.html", form=form)

        if user and verify_password(user["password_hash"], form.password.data):
            # #region agent log
            try:
                with open(_log_path, 'a') as f:
                    f.write(json.dumps({"location":"auth/routes.py:login","message":"Credentials verified, logging in user","data":{"username":form.username.data},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
            except: pass
            # #endregion
            
            # Login the user object
            login_user(User(user))

            # NORMAL LOGIN → always go to user dashboard
            return redirect(url_for("vault.dashboard"))

        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"auth/routes.py:login","message":"Invalid credentials","data":{"username":form.username.data},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
        except: pass
        # #endregion
        flash("Invalid credentials", "danger")
    else:
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"auth/routes.py:login","message":"Form validation failed or GET request","data":{"errors":form.errors if hasattr(form,'errors') else {},"method":request.method},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
        except: pass
        # #endregion

    return render_template("login.html", form=form)


# ---------------- ADMIN LOGIN PAGE ---------------- #
@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    # #region agent log
    import json, os, time
    _log_path = os.path.join(os.path.dirname(__file__), '..', '.cursor', 'debug.log')
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"auth/routes.py:admin_login","message":"admin_login route called","data":{"method":request.method},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
    except: pass
    # #endregion
    
    form = LoginForm()
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"auth/routes.py:admin_login","message":"LoginForm created","data":{"form_data":bool(request.form)},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
    except: pass
    # #endregion

    if form.validate_on_submit():
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"auth/routes.py:admin_login","message":"Form validated successfully","data":{"username":form.username.data},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
        except: pass
        # #endregion
        
        users = mongo.db.users
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"auth/routes.py:admin_login","message":"Attempting database query","data":{"username":form.username.data},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"G"})+"\n")
        except: pass
        # #endregion
        try:
            user = users.find_one({"username": form.username.data})
            # #region agent log
            try:
                with open(_log_path, 'a') as f:
                    f.write(json.dumps({"location":"auth/routes.py:admin_login","message":"Database query result","data":{"user_found":user is not None},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"G"})+"\n")
            except: pass
            # #endregion
        except Exception as db_err:
            # #region agent log
            try:
                with open(_log_path, 'a') as f:
                    f.write(json.dumps({"location":"auth/routes.py:admin_login","message":"Database query failed","data":{"error":str(db_err),"error_type":type(db_err).__name__},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"G"})+"\n")
            except: pass
            # #endregion
            flash("Database connection error. Please try again later.", "danger")
            return render_template("admin_login.html", form=form)

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
    else:
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"auth/routes.py:admin_login","message":"Form validation failed or GET request","data":{"errors":form.errors if hasattr(form,'errors') else {},"method":request.method},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"login-debug","hypothesisId":"F"})+"\n")
        except: pass
        # #endregion

    return render_template("admin_login.html", form=form)

# ---------------- LOGOUT ---------------- #
@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

# #region agent log - module import start
import json, os, time
_log_path = os.path.join(os.path.dirname(__file__), '.cursor', 'debug.log')
try:
    os.makedirs(os.path.dirname(_log_path), exist_ok=True)
    with open(_log_path, 'a') as f:
        f.write(json.dumps({"location":"app.py:1","message":"Module loading started","data":{},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"startup"})+"\n")
except: pass
# #endregion

from flask import Flask, redirect, url_for, render_template, jsonify
from config import Config
from extensions.mongo import mongo
from extensions.login import login_manager
from flask_jwt_extended import JWTManager

# Blueprints
try:
    from auth.routes import auth_bp
    from vault.routes import vault_bp
    from admin.routes import admin_bp
    from auth.api import auth_api_bp
    from vault.api import vault_api_bp
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:16","message":"All blueprints imported successfully","data":{},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"startup"})+"\n")
    except: pass
    # #endregion
except Exception as e:
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:18","message":"Blueprint import failed","data":{"error":str(e),"type":type(e).__name__},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"startup"})+"\n")
    except: pass
    # #endregion
    raise



def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:format_file_size","message":"format_file_size called","data":{"size_bytes":size_bytes,"type":str(type(size_bytes))},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"A"})+"\n")
    except: pass
    # #endregion
    # Handle None, empty, or zero values
    if size_bytes is None or size_bytes == 0:
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"app.py:format_file_size","message":"format_file_size returning 0B (edge case)","data":{"size_bytes":size_bytes},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"A"})+"\n")
        except: pass
        # #endregion
        return "0 B"
    
    try:
        size = float(size_bytes)
    except (ValueError, TypeError):
        # #region agent log
        try:
            with open(_log_path, 'a') as f:
                f.write(json.dumps({"location":"app.py:format_file_size","message":"format_file_size invalid input","data":{"size_bytes":size_bytes,"error":"ValueError or TypeError"},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"A"})+"\n")
        except: pass
        # #endregion
        return "0 B"
    
    # Handle negative numbers
    if size < 0:
        size = 0
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024
        i += 1
    
    result = f"{size:.2f} {size_names[i]}"
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:format_file_size","message":"format_file_size result","data":{"result":result,"original_bytes":size_bytes},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"A"})+"\n")
    except: pass
    # #endregion
    return result


def create_app():
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:create_app","message":"create_app starting","data":{},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"C"})+"\n")
    except: pass
    # #endregion
    app = Flask(__name__)
    app.config.from_object(Config)
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:create_app","message":"Flask app created and config loaded","data":{},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"C"})+"\n")
    except: pass
    # #endregion

    # Initialize extensions
    mongo.init_app(app)
    # #region agent log - test database connectivity
    db_connection_error = None
    try:
        db_status = {"db_available": hasattr(mongo, 'db')}
        if hasattr(mongo, 'db'):
            try:
                # Use a safe ping command to check server availability
                mongo.db.command("ping")
                db_status["connection_test"] = "success"
                db_status["mongo_uri"] = app.config.get('MONGO_URI', 'not set')
            except Exception as db_err:
                db_status["connection_test"] = "failed"
                db_status["error"] = str(db_err)
                db_status["error_type"] = type(db_err).__name__
                db_connection_error = db_err
                # Log warning to console
                import sys
                print(f"\n⚠️  WARNING: MongoDB connection failed!", file=sys.stderr)
                print(f"   Error: {type(db_err).__name__}", file=sys.stderr)
                print(f"   URI: {app.config.get('MONGO_URI', 'not set')}", file=sys.stderr)
                print(f"   Please ensure MongoDB is running and reachable from WSL.\n", file=sys.stderr)
        # Flag for routes/UI to know DB availability
        app.config["DB_AVAILABLE"] = (db_status.get("connection_test") == "success")
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:create_app","message":"mongo initialized","data":db_status,"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"E"})+"\n")
    except Exception as log_err:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:create_app","message":"mongo initialization check failed","data":{"error":str(log_err)},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"E"})+"\n")
    # #endregion
    login_manager.init_app(app)
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:create_app","message":"login_manager initialized","data":{},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"E"})+"\n")
    except: pass
    # #endregion
    jwt_manager = JWTManager(app)
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:create_app","message":"JWTManager initialized","data":{"jwt_manager_stored":jwt_manager is not None},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"D"})+"\n")
    except: pass
    # #endregion
    
    # Register Jinja filters
    app.jinja_env.filters['format_size'] = format_file_size
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:create_app","message":"Jinja filter registered","data":{"filter_exists":"format_size" in app.jinja_env.filters},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"B"})+"\n")
    except: pass
    # #endregion

    # REGISTER BLUEPRINTS HERE — INSIDE THE FUNCTION
    # REGISTER BLUEPRINTS — ONLY ONCE
    app.register_blueprint(auth_bp)
    app.register_blueprint(vault_bp)
    app.register_blueprint(auth_api_bp, url_prefix="/api")
    app.register_blueprint(vault_api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp)  # admin_bp ALREADY HAS /admin PREFIX INSIDE routes.py
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:create_app","message":"All blueprints registered","data":{"blueprint_count":len(app.blueprints)},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"C"})+"\n")
    except: pass
    # #endregion

    return app


try:
    app = create_app()
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:main","message":"app instance created","data":{"app_type":type(app).__name__},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"C"})+"\n")
    except: pass
    # #endregion
except Exception as e:
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:main","message":"create_app failed","data":{"error":str(e),"type":type(e).__name__},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"startup"})+"\n")
    except: pass
    # #endregion
    raise


@app.route("/")
def home():
    # #region agent log
    try:
        with open(_log_path, 'a') as f:
            f.write(json.dumps({"location":"app.py:home","message":"home route called","data":{},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"final","hypothesisId":"C"})+"\n")
    except: pass
    # #endregion
    return render_template("home.html")



@app.context_processor
def inject_flags():
    return {"DB_AVAILABLE": app.config.get("DB_AVAILABLE", False)}

@app.route("/health")
def health():
    try:
        mongo.db.command("ping")
        return jsonify({"status":"ok","db_available":True}), 200
    except Exception as e:
        return jsonify({"status":"degraded","db_available":False,"error":str(e)}), 503

if __name__ == "__main__":
    debug_env = os.environ.get("FLASK_DEBUG", "1")
    debug = debug_env.strip().lower() in ("1","true","t","yes","y","on")
    host = os.environ.get("HOST", "0.0.0.0")
    port_env = os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", "5000"))
    try:
        port = int(port_env)
    except ValueError:
        port = 5000
    app.run(host=host, port=port, debug=debug, use_reloader=False)

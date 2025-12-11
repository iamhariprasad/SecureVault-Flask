from flask import Flask, redirect, url_for, render_template
from config import Config
from extensions.mongo import mongo
from extensions.login import login_manager
from flask_jwt_extended import JWTManager

# Blueprints
from auth.routes import auth_bp
from vault.routes import vault_bp
from admin.routes import admin_bp
from auth.api import auth_api_bp
from vault.api import vault_api_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    login_manager.init_app(app)
    JWTManager(app)

    # REGISTER BLUEPRINTS HERE — INSIDE THE FUNCTION
    # REGISTER BLUEPRINTS — ONLY ONCE
    app.register_blueprint(auth_bp)
    app.register_blueprint(vault_bp)
    app.register_blueprint(auth_api_bp, url_prefix="/api")
    app.register_blueprint(vault_api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp)  # admin_bp ALREADY HAS /admin PREFIX INSIDE routes.py

    return app


app = create_app()


@app.route("/")
def home():
    return render_template("home.html")



if __name__ == "__main__":
    app.run(debug=True)

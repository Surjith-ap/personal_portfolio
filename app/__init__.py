import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = "Please log in to access the admin dashboard."


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)

    # Load config
    from config import config
    app.config.from_object(config.get(config_name, config["default"]))

    # Init extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Create tables on first run
    with app.app_context():
        db.create_all()

    return app

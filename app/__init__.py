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
        
        # Auto-seed if database is empty (first deployment)
        from app.models import Project, Skill, AdminUser
        if Project.query.first() is None:
            _seed_default_data()

    return app


def _seed_default_data():
    """Auto-seed default portfolio data on first startup."""
    from app.models import Project, Skill, AdminUser
    
    # Create admin user if none exists
    admin_user = os.environ.get("ADMIN_USERNAME", "admin")
    admin_pass = os.environ.get("ADMIN_PASSWORD", "admin123")
    
    if AdminUser.query.filter_by(username=admin_user).first() is None:
        new_admin = AdminUser(username=admin_user)
        new_admin.set_password(admin_pass)
        db.session.add(new_admin)
    
    # Seed projects
    projects_data = [
        {
            "title": "HireAI — AI Mock Interview Platform",
            "description": "A full-stack AI-driven interview practice platform that conducts adaptive mock interviews, analyzes real-time emotion and speech patterns via webcam, and generates personalised feedback using Gemini AI. Built as a team project; I designed and owned the entire backend.",
            "role": "Backend Lead — Express.js API, Python AI microservice, Clerk auth integration",
            "tech_stack": ["Next.js", "React", "Express.js", "Python", "PostgreSQL", "Clerk", "DeepFace", "Gemini AI"],
            "is_featured": True,
            "order": 1,
        },
        {
            "title": "PocketGuard — Personal Finance Manager",
            "description": "A MERN-stack financial management application for tracking expenses, setting budgets, and visualising spending patterns. I built the complete backend REST API and database layer.",
            "role": "Backend Developer — Node.js/Express API, MongoDB schema design, JWT auth",
            "tech_stack": ["React.js", "Express.js", "Node.js", "MongoDB", "JWT"],
            "is_featured": True,
            "order": 2,
        },
    ]
    
    for pdata in projects_data:
        if Project.query.filter_by(title=pdata["title"]).first() is None:
            p = Project(
                title=pdata["title"],
                description=pdata["description"],
                role=pdata.get("role", ""),
                is_featured=pdata.get("is_featured", False),
                order=pdata.get("order", 0),
            )
            p.tech_stack = pdata["tech_stack"]
            db.session.add(p)
    
    # Seed skills
    skills_data = [
        {"name": "Python", "category": "Language", "level": 88, "order": 1},
        {"name": "SQL", "category": "Language", "level": 78, "order": 2},
        {"name": "JavaScript", "category": "Language", "level": 70, "order": 3},
        {"name": "Flask", "category": "Framework", "level": 85, "order": 1},
        {"name": "Express.js", "category": "Framework", "level": 75, "order": 2},
        {"name": "React.js", "category": "Framework", "level": 68, "order": 3},
        {"name": "Git & GitHub", "category": "Tool", "level": 85, "order": 1},
        {"name": "REST API Design", "category": "Concept", "level": 85, "order": 1},
        {"name": "OOP", "category": "Concept", "level": 88, "order": 2},
    ]
    
    for sdata in skills_data:
        if Skill.query.filter_by(name=sdata["name"]).first() is None:
            s = Skill(**sdata)
            db.session.add(s)
    
    db.session.commit()

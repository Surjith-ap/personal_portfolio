import json
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


# ---------------------------------------------------------------------------
# Admin User (Flask-Login)
# ---------------------------------------------------------------------------

class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<AdminUser {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))


# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------

class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(200))                    # e.g., "Backend Lead"
    _tech_stack = db.Column("tech_stack", db.Text)      # JSON list of strings
    github_url = db.Column(db.String(300))
    live_url = db.Column(db.String(300))
    mermaid_diagram = db.Column(db.Text)                # Raw Mermaid code block
    backend_metrics = db.Column(db.Text)                # Highlighted metrics string
    _api_endpoints = db.Column("api_endpoints", db.Text)  # JSON list of dicts
    is_featured = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)            # Display ordering

    # --- tech_stack helpers ---
    @property
    def tech_stack(self):
        return json.loads(self._tech_stack) if self._tech_stack else []

    @tech_stack.setter
    def tech_stack(self, value):
        self._tech_stack = json.dumps(value)

    # --- api_endpoints helpers ---
    @property
    def api_endpoints(self):
        return json.loads(self._api_endpoints) if self._api_endpoints else []

    @api_endpoints.setter
    def api_endpoints(self, value):
        self._api_endpoints = json.dumps(value)

    def __repr__(self):
        return f"<Project {self.title}>"


# ---------------------------------------------------------------------------
# Skill
# ---------------------------------------------------------------------------

class Skill(db.Model):
    __tablename__ = "skill"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    # Category: Language | Framework | Tool | Concept | Cloud
    category = db.Column(db.String(60), nullable=False, default="Tool")
    level = db.Column(db.Integer, default=80)  # 0–100 for optional progress display
    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Skill {self.name}>"


# ---------------------------------------------------------------------------
# Contact Message
# ---------------------------------------------------------------------------

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200))
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Message from {self.email} at {self.sent_at}>"

import json
import re
import requests
from urllib import error as urllib_error
from urllib import request as urllib_request

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app import db
from app.models import Project, Skill, Message

main_bp = Blueprint("main", __name__)


# -------
# Helpers
# -------

def validate_contact_form(name, email, subject, body):
    """
    Validate contact form fields against industry-standard rules.
    Returns (is_valid: bool, error_message: str or None)
    """
    # Name validation: required, 2-100 characters, alphanumeric + common chars
    if not name or len(name) < 2:
        return False, "Name must be at least 2 characters."
    if len(name) > 100:
        return False, "Name must be 100 characters or fewer."
    if not re.match(r"^[a-zA-Z0-9\s.,'&-]+$", name):
        return False, "Name contains invalid characters."

    # Email validation: RFC 5322 simplified pattern
    email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    if not re.match(email_pattern, email):
        return False, "Please provide a valid email address."
    if len(email) > 254:
        return False, "Email address is too long."

    # Subject validation: optional, but if provided max 200 characters
    if subject and len(subject) > 200:
        return False, "Subject must be 200 characters or fewer."

    # Message validation: required, 10-5000 characters
    if not body or len(body) < 10:
        return False, "Message must be at least 10 characters."
    if len(body) > 5000:
        return False, "Message must be 5000 characters or fewer."

    return True, None


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

@main_bp.route("/")
def index():
    featured = Project.query.filter_by(is_featured=True).order_by(Project.order).all()
    # Group skills by category for the homepage snapshot
    skills = Skill.query.order_by(Skill.category, Skill.order).all()
    skill_groups = {}
    for skill in skills:
        skill_groups.setdefault(skill.category, []).append(skill)
    return render_template("index.html", featured=featured, skill_groups=skill_groups)


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

@main_bp.route("/about")
def about():
    skills = Skill.query.order_by(Skill.category, Skill.order).all()
    skill_groups = {}
    for skill in skills:
        skill_groups.setdefault(skill.category, []).append(skill)
    return render_template("about.html", skill_groups=skill_groups)


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

@main_bp.route("/projects")
def projects():
    all_projects = Project.query.order_by(Project.order).all()
    return render_template("projects.html", projects=all_projects)


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        email   = request.form.get("email", "").strip()
        subject = request.form.get("subject", "Portfolio Inquiry").strip()
        body    = request.form.get("body", "").strip()

        # Validate form data
        is_valid, error_msg = validate_contact_form(name, email, subject, body)
        if not is_valid:
            flash(error_msg, "error")
            return redirect(url_for("main.contact"))

        # Persist message to DB
        msg = Message(name=name, email=email, subject=subject, body=body)
        db.session.add(msg)
        db.session.commit()

        # Send email notification via Formspree over HTTPS so Render's SMTP block is avoided.
        try:
            formspree_form_id = current_app.config.get("FORMSPREE_FORM_ID")

            if formspree_form_id:
                payload = {
                    "name": name,
                    "email": email,
                    "subject": subject,
                    "message": body,
                }

                response = requests.post(
                    f"https://formspree.io/f/{formspree_form_id}",
                    json=payload,
                    headers={"Accept": "application/json"},
                    timeout=8
                )
                response.raise_for_status()
        except requests.RequestException as exc:
            current_app.logger.warning("Contact email send failed: %s", exc)
        except Exception as exc:
            # Email failure is non-fatal; message is already in DB.
            current_app.logger.warning("Contact email send failed: %s", exc)

        flash("Message sent! I'll get back to you soon.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html")

import json
import requests
from urllib import error as urllib_error
from urllib import request as urllib_request

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app import db
from app.models import Project, Skill, Message

main_bp = Blueprint("main", __name__)


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

        if not all([name, email, body]):
            flash("Please fill in all required fields.", "error")
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

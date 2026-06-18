from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Message as MailMessage
from app import db, mail
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

        # Send email notification
        try:
            email_msg = MailMessage(
                subject=f"[Portfolio] {subject}",
                recipients=["surjith.ap007@gmail.com"],
                body=f"From: {name} <{email}>\n\n{body}",
                reply_to=email,
            )
            mail.send(email_msg)
        except Exception:
            # Email failure is non-fatal; message is already in DB
            pass

        flash("Message sent! I'll get back to you soon.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html")

import smtplib
from email.message import EmailMessage

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

        # Send email notification with a short timeout so the request cannot hang.
        try:
            smtp_username = current_app.config.get("MAIL_USERNAME")
            smtp_password = current_app.config.get("MAIL_PASSWORD")
            mail_enabled = bool(smtp_username and smtp_password)

            if mail_enabled:
                email_msg = EmailMessage()
                email_msg["Subject"] = f"[Portfolio] {subject}"
                email_msg["From"] = current_app.config.get("MAIL_DEFAULT_SENDER") or smtp_username
                email_msg["To"] = "surjith.ap007@gmail.com"
                email_msg["Reply-To"] = email
                email_msg.set_content(f"From: {name} <{email}>\n\n{body}")

                with smtplib.SMTP("smtp.gmail.com", 587, timeout=8) as smtp:
                    smtp.starttls()
                    smtp.login(smtp_username, smtp_password)
                    smtp.send_message(email_msg)
        except Exception as exc:
            # Email failure is non-fatal; message is already in DB.
            current_app.logger.warning("Contact email send failed: %s", exc)

        flash("Message sent! I'll get back to you soon.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html")

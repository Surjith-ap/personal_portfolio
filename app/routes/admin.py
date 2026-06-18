import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import AdminUser, Project, Skill, Message

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "error")

    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@admin_bp.route("/")
@login_required
def dashboard():
    projects = Project.query.order_by(Project.order).all()
    skills   = Skill.query.order_by(Skill.category, Skill.order).all()
    messages = Message.query.order_by(Message.sent_at.desc()).limit(10).all()
    unread   = Message.query.filter_by(is_read=False).count()
    return render_template(
        "admin/dashboard.html",
        projects=projects, skills=skills,
        messages=messages, unread=unread,
    )


# ---------------------------------------------------------------------------
# Projects CRUD
# ---------------------------------------------------------------------------

@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def new_project():
    if request.method == "POST":
        p = Project(
            title=request.form["title"],
            description=request.form["description"],
            role=request.form.get("role", ""),
            github_url=request.form.get("github_url", ""),
            live_url=request.form.get("live_url", ""),
            mermaid_diagram=request.form.get("mermaid_diagram", ""),
            backend_metrics=request.form.get("backend_metrics", ""),
            is_featured=bool(request.form.get("is_featured")),
            order=int(request.form.get("order", 0)),
        )
        # Parse comma-separated tech stack
        tech_raw = request.form.get("tech_stack", "")
        p.tech_stack = [t.strip() for t in tech_raw.split(",") if t.strip()]

        # Parse JSON endpoints (may be empty)
        ep_raw = request.form.get("api_endpoints", "[]")
        try:
            p.api_endpoints = json.loads(ep_raw)
        except json.JSONDecodeError:
            p.api_endpoints = []

        db.session.add(p)
        db.session.commit()
        flash(f'Project "{p.title}" created.', "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_project.html", project=None)


@admin_bp.route("/projects/<int:pid>/edit", methods=["GET", "POST"])
@login_required
def edit_project(pid):
    p = Project.query.get_or_404(pid)

    if request.method == "POST":
        p.title          = request.form["title"]
        p.description    = request.form["description"]
        p.role           = request.form.get("role", "")
        p.github_url     = request.form.get("github_url", "")
        p.live_url       = request.form.get("live_url", "")
        p.mermaid_diagram = request.form.get("mermaid_diagram", "")
        p.backend_metrics = request.form.get("backend_metrics", "")
        p.is_featured    = bool(request.form.get("is_featured"))
        p.order          = int(request.form.get("order", 0))

        tech_raw = request.form.get("tech_stack", "")
        p.tech_stack = [t.strip() for t in tech_raw.split(",") if t.strip()]

        ep_raw = request.form.get("api_endpoints", "[]")
        try:
            p.api_endpoints = json.loads(ep_raw)
        except json.JSONDecodeError:
            p.api_endpoints = []

        db.session.commit()
        flash(f'Project "{p.title}" updated.', "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_project.html", project=p)


@admin_bp.route("/projects/<int:pid>/delete", methods=["POST"])
@login_required
def delete_project(pid):
    p = Project.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash(f'Project "{p.title}" deleted.', "success")
    return redirect(url_for("admin.dashboard"))


# ---------------------------------------------------------------------------
# Skills CRUD
# ---------------------------------------------------------------------------

@admin_bp.route("/skills/new", methods=["GET", "POST"])
@login_required
def new_skill():
    if request.method == "POST":
        s = Skill(
            name=request.form["name"],
            category=request.form.get("category", "Tool"),
            level=int(request.form.get("level", 80)),
            order=int(request.form.get("order", 0)),
        )
        db.session.add(s)
        db.session.commit()
        flash(f'Skill "{s.name}" added.', "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/edit_skill.html", skill=None)


@admin_bp.route("/skills/<int:sid>/edit", methods=["GET", "POST"])
@login_required
def edit_skill(sid):
    s = Skill.query.get_or_404(sid)
    if request.method == "POST":
        s.name     = request.form["name"]
        s.category = request.form.get("category", "Tool")
        s.level    = int(request.form.get("level", 80))
        s.order    = int(request.form.get("order", 0))
        db.session.commit()
        flash(f'Skill "{s.name}" updated.', "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/edit_skill.html", skill=s)


@admin_bp.route("/skills/<int:sid>/delete", methods=["POST"])
@login_required
def delete_skill(sid):
    s = Skill.query.get_or_404(sid)
    db.session.delete(s)
    db.session.commit()
    flash(f'Skill "{s.name}" deleted.', "success")
    return redirect(url_for("admin.dashboard"))


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------

@admin_bp.route("/messages/<int:mid>/read", methods=["POST"])
@login_required
def mark_read(mid):
    m = Message.query.get_or_404(mid)
    m.is_read = True
    db.session.commit()
    return redirect(url_for("admin.dashboard"))

"""
Run once to seed the database with resume data and create your admin account.

    python seed.py

This is safe to re-run — it won't duplicate entries.
"""
import os
import getpass
from app import create_app, db
from app.models import AdminUser, Project, Skill

app = create_app(os.environ.get("FLASK_ENV", "development"))

HIREAI_MERMAID = """graph LR
    A[Browser / Client] -->|HTTPS| B[Next.js Frontend]
    B -->|REST API| C[Express.js Backend]
    C -->|Auth Check| D[Clerk Auth Service]
    C -->|Interview Data| E[PostgreSQL Database]
    C -->|HTTP| F[Python Microservice]
    F -->|DeepFace| G[Emotion Analyzer]
    F -->|Gemini AI| H[Response Generator]
    G --> F
    H --> F
    F -->|JSON Response| C"""

POCKETGUARD_MERMAID = """graph LR
    A[React Client] -->|REST API| B[Express.js Server]
    B -->|JWT Middleware| C{Auth Valid?}
    C -->|Yes| D[Route Handlers]
    C -->|No| E[401 Unauthorized]
    D -->|Mongoose ODM| F[MongoDB Atlas]
    F -->|Documents| D
    D -->|JSON| A"""

PROJECTS = [
    {
        "title": "HireAI — AI Mock Interview Platform",
        "description": (
            "A full-stack AI-driven interview practice platform that conducts "
            "adaptive mock interviews, analyzes real-time emotion and speech patterns "
            "via webcam, and generates personalised feedback using Gemini AI. "
            "Built as a team project; I designed and owned the entire backend."
        ),
        "role": "Backend Lead — Express.js API, Python AI microservice, Clerk auth integration",
        "tech_stack": ["Next.js", "React", "Express.js", "Python", "PostgreSQL", "Clerk", "DeepFace", "Gemini AI"],
        "github_url": "",
        "live_url": "",
        "mermaid_diagram": HIREAI_MERMAID,
        "backend_metrics": (
            "Real-time video-frame emotion pipeline with sub-200 ms round-trip latency. "
            "Stateless JWT sessions via Clerk — zero server-side session storage. "
            "Structured PostgreSQL schema with indexed session lookups for fast result retrieval."
        ),
        "api_endpoints": [
            {"method": "POST", "path": "/api/interview/start",    "desc": "Initialise a new interview session"},
            {"method": "POST", "path": "/api/analysis/emotion",   "desc": "Receive frame data, return emotion JSON"},
            {"method": "POST", "path": "/api/analysis/speech",    "desc": "Transcribe audio, evaluate response quality"},
            {"method": "GET",  "path": "/api/results/:sessionId", "desc": "Fetch full interview report"},
        ],
        "is_featured": True,
        "order": 1,
    },
    {
        "title": "PocketGuard — Personal Finance Manager",
        "description": (
            "A MERN-stack financial management application for tracking expenses, "
            "setting budgets, and visualising spending patterns. I built the complete "
            "backend REST API and database layer."
        ),
        "role": "Backend Developer — Node.js/Express API, MongoDB schema design, JWT auth",
        "tech_stack": ["React.js", "Express.js", "Node.js", "MongoDB", "JWT"],
        "github_url": "",
        "live_url": "",
        "mermaid_diagram": POCKETGUARD_MERMAID,
        "backend_metrics": (
            "JWT-secured REST API with role-based middleware protecting all write routes. "
            "MongoDB aggregation pipeline for monthly budget summaries — single query replacing "
            "multiple round-trips. Bcrypt-hashed credentials with salted rounds."
        ),
        "api_endpoints": [
            {"method": "POST", "path": "/api/auth/register",      "desc": "Create user account"},
            {"method": "POST", "path": "/api/auth/login",         "desc": "Return signed JWT"},
            {"method": "GET",  "path": "/api/expenses",           "desc": "List expenses (paginated, filterable)"},
            {"method": "POST", "path": "/api/expenses",           "desc": "Add new expense entry"},
            {"method": "GET",  "path": "/api/budget/summary",     "desc": "Aggregated monthly budget report"},
        ],
        "is_featured": True,
        "order": 2,
    },
    {
        "title": "Ransomware Simulation Tool",
        "description": (
            "Developed during the C-DAC internship to test and analyse system defence "
            "capabilities. The tool simulates ransomware behaviour in a sandboxed environment, "
            "helping security teams evaluate detection and response time without real risk."
        ),
        "role": "Solo Developer — Python scripting, encryption logic, sandboxed execution",
        "tech_stack": ["Python", "Cryptography", "Network Security"],
        "github_url": "",
        "live_url": "",
        "mermaid_diagram": """graph TD
    A[Simulation Start] --> B[Enumerate Target Files]
    B --> C[AES Encrypt in Sandbox]
    C --> D[Drop Ransom Note]
    D --> E[Log to Audit Trail]
    E --> F[Alert Security Monitor]
    F --> G[Measure Response Time]""",
        "backend_metrics": (
            "Sandboxed execution prevents any real system impact. "
            "AES encryption layer for realistic payload simulation. "
            "Automated audit logging to measure mean detection and response time."
        ),
        "api_endpoints": [],
        "is_featured": False,
        "order": 3,
    },
]

SKILLS = [
    # Languages
    {"name": "Python",  "category": "Language", "level": 88, "order": 1},
    {"name": "SQL",     "category": "Language", "level": 78, "order": 2},
    {"name": "C",       "category": "Language", "level": 65, "order": 3},
    {"name": "JavaScript", "category": "Language", "level": 70, "order": 4},
    # Frameworks
    {"name": "Flask",       "category": "Framework", "level": 85, "order": 1},
    {"name": "Express.js",  "category": "Framework", "level": 75, "order": 2},
    {"name": "Next.js",     "category": "Framework", "level": 65, "order": 3},
    {"name": "React.js",    "category": "Framework", "level": 68, "order": 4},
    # Libraries
    {"name": "Pandas",      "category": "Library", "level": 80, "order": 1},
    {"name": "SQLAlchemy",  "category": "Library", "level": 78, "order": 2},
    {"name": "DeepFace",    "category": "Library", "level": 65, "order": 3},
    {"name": "scikit-learn","category": "Library", "level": 72, "order": 4},
    # Tools
    {"name": "Git & GitHub",    "category": "Tool", "level": 85, "order": 1},
    {"name": "VS Code",         "category": "Tool", "level": 90, "order": 2},
    {"name": "Jupyter Notebook","category": "Tool", "level": 82, "order": 3},
    {"name": "PyCharm",         "category": "Tool", "level": 75, "order": 4},
    {"name": "Postman",         "category": "Tool", "level": 78, "order": 5},
    # Concepts
    {"name": "REST API Design",        "category": "Concept", "level": 85, "order": 1},
    {"name": "OOP",                    "category": "Concept", "level": 88, "order": 2},
    {"name": "Data Structures & Algo", "category": "Concept", "level": 75, "order": 3},
    {"name": "JWT Auth",               "category": "Concept", "level": 80, "order": 4},
    {"name": "Penetration Testing",    "category": "Concept", "level": 70, "order": 5},
    # Cloud / AI
    {"name": "Gemini AI",       "category": "Cloud & AI", "level": 75, "order": 1},
    {"name": "Oracle Cloud AI", "category": "Cloud & AI", "level": 72, "order": 2},
    {"name": "Ollama (Local LLM)", "category": "Cloud & AI", "level": 78, "order": 3},
    {"name": "SQLite / PostgreSQL / MongoDB", "category": "Cloud & AI", "level": 80, "order": 4},
]


def seed():
    with app.app_context():
        # --- Admin user ---
        print("\n=== Admin Account Setup ===")
        username = input("Enter admin username: ").strip()
        password = getpass.getpass("Enter admin password: ")
        confirm  = getpass.getpass("Confirm admin password: ")

        if password != confirm:
            print("Passwords do not match. Aborting.")
            return

        existing = AdminUser.query.filter_by(username=username).first()
        if existing:
            print(f"Admin '{username}' already exists. Skipping.")
        else:
            admin = AdminUser(username=username)
            admin.set_password(password)
            db.session.add(admin)
            print(f"Admin '{username}' created.")

        # --- Projects ---
        for data in PROJECTS:
            if not Project.query.filter_by(title=data["title"]).first():
                p = Project(
                    title=data["title"],
                    description=data["description"],
                    role=data["role"],
                    github_url=data["github_url"],
                    live_url=data["live_url"],
                    mermaid_diagram=data["mermaid_diagram"],
                    backend_metrics=data["backend_metrics"],
                    is_featured=data["is_featured"],
                    order=data["order"],
                )
                p.tech_stack    = data["tech_stack"]
                p.api_endpoints = data["api_endpoints"]
                db.session.add(p)
                print(f"  + Project: {data['title']}")

        # --- Skills ---
        for data in SKILLS:
            if not Skill.query.filter_by(name=data["name"]).first():
                s = Skill(**data)
                db.session.add(s)
                print(f"  + Skill: {data['name']}")

        db.session.commit()
        print("\nSeed complete. Run:  flask run")


if __name__ == "__main__":
    seed()

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-change-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Resend (HTTP API, works on Render free tier)
    # RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
    # RESEND_FROM_EMAIL = os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev")
    # CONTACT_RECIPIENT_EMAIL = os.environ.get("CONTACT_RECIPIENT_EMAIL", "surjith.ap007@gmail.com")
    WEB3FORMS_ACCESS_KEY = os.environ.get("WEB3FORMS_ACCESS_KEY")

    # Admin credentials (seeded once via `flask seed-admin`)
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///portfolio_dev.db"


class ProductionConfig(Config):
    DEBUG = False
    # Render provides a persistent disk; SQLite path must be absolute.
    # Set DATABASE_URL env var on Render if you migrate to Postgres later.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:////opt/render/project/src/portfolio.db"
    )


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

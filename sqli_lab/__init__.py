import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from sqli_lab.models import db
from sqli_lab.routes import register_blueprints
from sqli_lab.lab_db import init_lab_tables


def create_app(test_config: dict | None = None) -> Flask:
    load_dotenv()
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).resolve().parent.parent / "templates"),
        static_folder=str(Path(__file__).resolve().parent.parent / "static"),
    )

    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    app.config.update(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "dev-only-insecure-key-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL", f"sqlite:///{data_dir / 'sqli_lab.db'}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=60 * 60 * 8,
        LAB_DB_PATH=str(data_dir / "sqli_lab.db"),
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        init_lab_tables(app.config["LAB_DB_PATH"])

    register_blueprints(app)

    @app.context_processor
    def inject_user():
        from sqli_lab.auth_utils import current_user

        return {"user": current_user()}

    return app

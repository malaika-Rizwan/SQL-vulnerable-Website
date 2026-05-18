import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, g

from sqli_lab.models import db
from sqli_lab.routes import register_blueprints
from sqli_lab.lab_db import init_lab_tables

_db_ready = False


def _on_vercel() -> bool:
    return bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))


def _storage_paths() -> tuple[Path, str, str]:
    """Use /tmp on Vercel serverless (ephemeral, writable)."""
    if _on_vercel():
        lab_db_path = "/tmp/sqli_lab.db"
        db_uri = os.getenv("DATABASE_URL", "sqlite:////tmp/sqli_lab.db")
        return Path("/tmp"), db_uri, lab_db_path

    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    db_file = data_dir / "sqli_lab.db"
    db_uri = os.getenv("DATABASE_URL", f"sqlite:///{db_file.as_posix()}")
    return data_dir, db_uri, str(db_file)


def _ensure_database(app: Flask) -> None:
    global _db_ready
    if _db_ready and not app.config.get("TESTING"):
        return
    with app.app_context():
        db.create_all()
        init_lab_tables(app.config["LAB_DB_PATH"])
        from sqli_lab.seed_db import seed_if_empty

        seed_if_empty()
    _db_ready = True


def create_app(test_config: dict | None = None) -> Flask:
    load_dotenv()
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).resolve().parent.parent / "templates"),
        static_folder=str(Path(__file__).resolve().parent.parent / "static"),
    )

    _data_dir, db_uri, lab_db_path = _storage_paths()
    on_vercel = _on_vercel()

    app.config.update(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "dev-only-insecure-key-change-me"),
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            "connect_args": {"check_same_thread": False},
            "pool_pre_ping": True,
        },
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=on_vercel,
        PERMANENT_SESSION_LIFETIME=60 * 60 * 8,
        LAB_DB_PATH=lab_db_path,
    )
    if test_config:
        global _db_ready
        _db_ready = False
        app.config.update(test_config)
        db.init_app(app)
        register_blueprints(app)
        _ensure_database(app)

        @app.context_processor
        def inject_user():
            from sqli_lab.auth_utils import current_user

            return {"user": current_user()}

        return app

    db.init_app(app)
    register_blueprints(app)

    @app.before_request
    def _init_db_once():
        if not g.get("db_initialized"):
            _ensure_database(app)
            g.db_initialized = True

    @app.context_processor
    def inject_user():
        from sqli_lab.auth_utils import current_user

        return {"user": current_user()}

    return app

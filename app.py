"""Vercel entrypoint — exposes WSGI `app` (see pyproject.toml)."""

import os
import traceback

from flask import Flask

_app = None


def _build_app():
    from sqli_lab import create_app

    return create_app()


try:
    app = _build_app()
except Exception:
    # Fallback app so Vercel logs show the real error instead of a blank crash
    app = Flask(__name__)

    @app.route("/")
    def _startup_error():
        return (
            "<h1>SQLi Lab failed to start</h1>"
            "<pre>"
            + traceback.format_exc()
            + "</pre>"
            "<p>Set FLASK_SECRET_KEY in Vercel Environment Variables and redeploy.</p>"
        ), 500

    @app.route("/<path:_path>")
    def _startup_error_any(_path):
        return _startup_error()

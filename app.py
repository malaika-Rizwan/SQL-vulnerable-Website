"""Vercel entrypoint — exposes WSGI `app` (see pyproject.toml)."""

from sqli_lab import create_app

app = create_app()

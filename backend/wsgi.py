"""WSGI entrypoint for gunicorn / Render deployment."""

from .app import create_app

application = create_app()

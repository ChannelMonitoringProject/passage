from flask import Flask
from . import routes


def create_app():
    app = Flask(__name__)

    from .routes import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/")

    return app

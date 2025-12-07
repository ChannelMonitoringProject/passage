from flask import Flask
from . import routes
from api.utils.redis_helper import create_index_if_missing


def create_app():
    app = Flask(__name__)
    from .routes import bp as api_bp

    create_index_if_missing()

    app.register_blueprint(api_bp, url_prefix="/")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=80)

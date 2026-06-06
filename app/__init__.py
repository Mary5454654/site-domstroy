from pathlib import Path

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "study-practice-secret-key"
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    from .routes import main

    app.register_blueprint(main)
    return app

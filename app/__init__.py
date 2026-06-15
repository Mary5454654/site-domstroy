import secrets
from pathlib import Path

from flask import Flask


def create_app():
    app = Flask(__name__)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    # Ключ создается на хостинге и не хранится в публичном репозитории.
    secret_path = Path(app.instance_path) / ".secret_key"
    if not secret_path.exists():
        secret_path.write_text(secrets.token_hex(32), encoding="utf-8")
    app.config["SECRET_KEY"] = secret_path.read_text(encoding="utf-8").strip()

    from .routes import main

    app.register_blueprint(main)
    return app

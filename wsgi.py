# -*- coding: utf-8 -*-
import sys
from pathlib import Path


# Пути определяются автоматически после загрузки проекта на SpaceWeb.
PROJECT_DIR = Path(__file__).resolve().parent
VENDOR_DIR = PROJECT_DIR / "vendor"

sys.path.insert(0, str(VENDOR_DIR))
sys.path.insert(0, str(PROJECT_DIR))

from app import create_app


flask_app = create_app()


def application(environ, start_response):
    # mod_wsgi запускает файл как /wsgi.py, но сайт опубликован в корне домена.
    environ["SCRIPT_NAME"] = ""
    return flask_app(environ, start_response)

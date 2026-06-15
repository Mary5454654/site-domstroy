# -*- coding: utf-8 -*-
import sys
from pathlib import Path


# Пути определяются автоматически после загрузки проекта на SpaceWeb.
PROJECT_DIR = Path(__file__).resolve().parent
VENDOR_DIR = PROJECT_DIR / "vendor"

sys.path.insert(0, str(VENDOR_DIR))
sys.path.insert(0, str(PROJECT_DIR))

from app import create_app


application = create_app()

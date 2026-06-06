import json
from pathlib import Path

from flask import current_app


DEFAULT_USERS = [
    {
        "login": "admin",
        "password": "admin123",
        "name": "Администратор",
        "role": "admin",
    },
    {
        "login": "manager",
        "password": "manager123",
        "name": "Сотрудник",
        "role": "employee",
    },
    {
        "login": "client",
        "password": "client123",
        "name": "Клиент",
        "role": "client",
    },
]


ROLE_NAMES = {
    "admin": "Администратор",
    "employee": "Сотрудник",
    "client": "Клиент",
}


def _path(filename):
    return Path(current_app.instance_path) / filename


def _read_json(filename, default):
    path = _path(filename)
    if not path.exists():
        _write_json(filename, default)
        return default.copy() if isinstance(default, list) else default
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _write_json(filename, data):
    path = _path(filename)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users():
    return _read_json("users.json", DEFAULT_USERS)


def save_users(users):
    _write_json("users.json", users)


def find_user(login):
    for user in load_users():
        if user["login"] == login:
            return user
    return None


def authenticate(login, password):
    user = find_user(login)
    if user and user["password"] == password:
        return user
    return None


def add_user(login, password, name, role="client"):
    users = load_users()
    if any(user["login"] == login for user in users):
        return False, "Пользователь с таким логином уже существует."
    users.append(
        {
            "login": login,
            "password": password,
            "name": name,
            "role": role,
        }
    )
    save_users(users)
    return True, "Пользователь создан."


def load_messages():
    return _read_json("messages.json", [])


def add_message(name, email, topic, text):
    messages = load_messages()
    messages.append(
        {
            "name": name,
            "email": email,
            "topic": topic,
            "text": text,
        }
    )
    _write_json("messages.json", messages)

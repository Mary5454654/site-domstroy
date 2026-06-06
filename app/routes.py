from flask import Blueprint, render_template

from .data import PROJECTS, SERVICES, SITE_PAGES


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html", title="Главная")


@main.app_context_processor
def inject_menu():
    return {"site_pages": SITE_PAGES}


@main.route("/projects/")
def projects():
    return render_template("projects.html", title="Проекты", projects=PROJECTS)


@main.route("/services/")
def services():
    return render_template("services.html", title="Услуги", services=SERVICES)


@main.route("/articles/")
def articles():
    return render_template("articles.html", title="Статьи")


@main.route("/news/")
def news():
    return render_template("news.html", title="Новости")


@main.route("/contacts/")
def contacts():
    return render_template("contacts.html", title="Контакты")


@main.route("/account/")
def account():
    return render_template("account.html", title="Кабинет")


@main.route("/search/")
def search():
    return render_template("search.html", title="Поиск", query="", results=[])


@main.route("/sitemap/")
def sitemap():
    return render_template("sitemap.html", title="Карта сайта")


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="Страница не найдена"), 404

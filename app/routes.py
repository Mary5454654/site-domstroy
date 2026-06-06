from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from .data import ARTICLES, NEWS, PROJECTS, SERVICES, SITE_PAGES, get_article, searchable_items
from .storage import ROLE_NAMES, add_message, add_user, authenticate, load_messages


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template(
        "index.html",
        title="Главная",
        projects=PROJECTS[:3],
        news=NEWS[:3],
    )


@main.app_context_processor
def inject_menu():
    return {"site_pages": SITE_PAGES, "current_user": session.get("user")}


@main.route("/projects/")
def projects():
    return render_template("projects.html", title="Проекты", projects=PROJECTS)


@main.route("/services/")
def services():
    return render_template("services.html", title="Услуги", services=SERVICES)


@main.route("/articles/")
def articles():
    return render_template("articles.html", title="Статьи", articles=ARTICLES)


@main.route("/articles/<slug>/")
def article_detail(slug):
    article = get_article(slug)
    if article is None:
        abort(404)
    return render_template("article_detail.html", title=article["title"], article=article)


@main.route("/news/")
def news():
    return render_template("news.html", title="Новости", news=NEWS)


@main.route("/contacts/", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        topic = request.form.get("topic", "").strip()
        text = request.form.get("text", "").strip()
        if not name or not email or not text:
            flash("Заполните имя, email и текст сообщения.")
        else:
            add_message(name, email, topic, text)
            flash("Сообщение отправлено. Сотрудник свяжется с вами.")
            return redirect(url_for("main.contacts"))
    return render_template("contacts.html", title="Контакты")


@main.route("/account/", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "login":
            login = request.form.get("login", "").strip()
            password = request.form.get("password", "").strip()
            user = authenticate(login, password)
            if user is None:
                flash("Неверный логин или пароль.")
            else:
                session["user"] = {
                    "login": user["login"],
                    "name": user["name"],
                    "role": user["role"],
                }
                flash("Вход выполнен.")
                return redirect(url_for("main.account"))
        if action == "create_user":
            current_user = session.get("user")
            if not current_user or current_user["role"] not in ("admin", "employee"):
                abort(403)
            login = request.form.get("login", "").strip()
            password = request.form.get("password", "").strip()
            name = request.form.get("name", "").strip()
            role = request.form.get("role", "client")
            if not login or not password or not name:
                flash("Заполните все поля для создания пользователя.")
            elif role not in ROLE_NAMES:
                flash("Выбрана неизвестная роль.")
            else:
                ok, message = add_user(login, password, name, role)
                flash(message)
                if ok:
                    return redirect(url_for("main.account"))

    current = session.get("user")
    messages = load_messages() if current and current["role"] in ("admin", "employee") else []
    return render_template(
        "account.html",
        title="Кабинет",
        role_names=ROLE_NAMES,
        messages=messages,
    )


@main.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login", "").strip()
        password = request.form.get("password", "").strip()
        name = request.form.get("name", "").strip()
        if not login or not password or not name:
            flash("Заполните имя, логин и пароль.")
        else:
            ok, message = add_user(login, password, name, "client")
            flash(message)
            if ok:
                return redirect(url_for("main.account"))
    return render_template("register.html", title="Регистрация")


@main.route("/logout/")
def logout():
    session.pop("user", None)
    flash("Вы вышли из кабинета.")
    return redirect(url_for("main.index"))


@main.route("/search/")
def search():
    query = request.args.get("q", "").strip()
    results = []
    if query:
        query_lower = query.lower()
        for item in searchable_items():
            search_text = f"{item['title']} {item['text']}".lower()
            if query_lower in search_text:
                if item["endpoint"] == "main.article_detail":
                    item["url"] = url_for(item["endpoint"], slug=item["slug"])
                else:
                    item["url"] = url_for(item["endpoint"])
                results.append(item)
    return render_template("search.html", title="Поиск", query=query, results=results)


@main.route("/sitemap/")
def sitemap():
    return render_template("sitemap.html", title="Карта сайта")


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="Страница не найдена"), 404

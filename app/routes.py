from flask import Blueprint, abort, render_template, request, url_for

from .data import ARTICLES, NEWS, PROJECTS, SERVICES, SITE_PAGES, get_article, searchable_items


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
    return {"site_pages": SITE_PAGES}


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


@main.route("/contacts/")
def contacts():
    return render_template("contacts.html", title="Контакты")


@main.route("/account/")
def account():
    return render_template("account.html", title="Кабинет")


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

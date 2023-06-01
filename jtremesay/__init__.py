import datetime
import importlib
from pathlib import Path
import os
import re

from flask import Flask, render_template, abort, url_for, current_app
from jinja2 import Template
from jinja2.exceptions import TemplateNotFound

re_post_entry = re.compile(r"(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_(?P<slug>\w+)\.html")

def get_posts_data():
    posts_path = importlib.resources.files("jtremesay.templates.blog")
    posts = []
    for post_entry in posts_path.iterdir():
        if not post_entry.is_file():
            continue

        match = re_post_entry.match(post_entry.name)
        if not match:
            continue

        groups = match.groupdict()
        year = int(groups["year"])
        month = int(groups["month"])
        day = int(groups["day"])
        slug = groups["slug"]

        ast = current_app.jinja_env.parse(Path(post_entry).read_text())
        for node in ast.body:
            if node.__class__.__name__ == "Block" and node.name == "title":
                title = node.body[0].nodes[0].data
                break
        else:
            continue

        post = {
            "pubdate": datetime.date(year, month, day),
            "slug": slug,
            "title": title,
            "url": url_for("view_post", year=year, month=month, day=day, slug=slug)
        
        }
        posts.append(post)

    return posts


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", defaults={"page": "index"})
    @app.route("/<string:page>")
    def view_page(page: str) -> str:
        try:
            return render_template(f"pages/{page}.html")
        except TemplateNotFound:
            abort(404)

    @app.route("/blog/")
    def list_posts() -> str:
        posts = get_posts_data()
        return render_template("list_posts.html", posts=posts)

    @app.route("/<int:year>/<int:month>/<int:day>/<slug>")
    def view_post(year: int, month: int, day: int, slug: str):
        try:
            return render_template(f"blog/{year:04}{month:02}{day:02}_{slug}.html")
        except TemplateNotFound:
            return abort(404)

    return app
import datetime
from pathlib import Path
import os
import re
import csv

from flask import Flask, render_template, abort, url_for, current_app
from jinja2.exceptions import TemplateNotFound
from jinja2 import Environment, PackageLoader, select_autoescape

APP_DIR = Path(__file__).parent

def get_posts_data():
    posts = []
    re_post_path = re.compile(r"(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_(?P<slug>\w+)\.html")
    env = Environment(
        loader=PackageLoader(__name__),
        autoescape=select_autoescape()
    )

    # That kind of ugly, but that works.
    # Initially, I tried to search posts with importlib.ressources,
    # but the module is not available when running the app with hypercorn ?!
    for post_path in APP_DIR.glob("templates/blog/*.html"):
        match = re_post_path.match(post_path.name)
        if not match:
            continue

        groups = match.groupdict()
        try:
            year = int(groups["year"])
            month = int(groups["month"])
            day = int(groups["day"])
        except ValueError:
            continue
        slug = groups["slug"]

        ast = env.parse(post_path.read_text())
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
        
        }
        posts.append(post)

    return posts

def get_youtube_channels() -> dict[str, str]:
    with (APP_DIR / "static" / "files" / "youtube_channels.csv").open() as f:
        reader = csv.DictReader(f)
        return list(reader)

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
    
    # Pre-loads the posts for faster generation of posts list
    POSTS = sorted(get_posts_data(), key=lambda k: k["pubdate"], reverse=True)  
    YOUTUBE_CHANNELS = get_youtube_channels()

    @app.route("/blog/")
    def list_posts() -> str:
        return render_template("base/list_posts.html", posts=POSTS)

    @app.route("/blog/<int:year>/<int:month>/<int:day>/<slug>")
    def view_post(year: int, month: int, day: int, slug: str):
        ctx = {}
        ctx["youtube_channels"] = YOUTUBE_CHANNELS

        try:
            return render_template(f"blog/{year:04}{month:02}{day:02}_{slug}.html", **ctx)
        except TemplateNotFound:
            return abort(404)
    
    @app.route("/atom.xml")
    def view_atom_feed():
        return render_template(f"base/atom.xml", posts=POSTS), {
            "Content-Type": "application/xml"
        } 

    @app.route("/", defaults={"page": "index"})
    @app.route("/<string:page>")
    def view_page(page: str) -> str:
        try:
            return render_template(f"pages/{page}.html")
        except TemplateNotFound:
            abort(404)

    return app
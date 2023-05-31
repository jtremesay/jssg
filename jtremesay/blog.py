from flask import (
    Blueprint, render_template, abort, url_for
)
from jinja2.exceptions import TemplateNotFound
import importlib
import re

re_post_entry = re.compile(r"(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_(?P<slug>\w+)\.html")

bp = Blueprint('blog', __name__)



@bp.route("/")
def index():
    posts_path = importlib.resources.files("jtremesay.templates.blog.posts")
    entries = []
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
        entries.append({
            "year": year,
            "month": month,
            "day": day,
            "slug": slug,
            "url": url_for("blog.post", year=year, month=month, day=day, slug=slug)
        })

    return render_template(f"blog/index.html", entries=entries)

@bp.route("/<int:year>/<int:month>/<int:day>/<slug>")
def post(year: int, month: int, day: int, slug: str):
    try:
        return render_template(f"blog/posts/{year:04}{month:02}{day:02}_{slug}.html")
    except TemplateNotFound:
        return abort(404)
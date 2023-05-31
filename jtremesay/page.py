from flask import (
    Blueprint, render_template, abort
)
from jinja2.exceptions import TemplateNotFound

bp = Blueprint('page', __name__)

@bp.route("/<page>")
def page(page:str=""):
    if not page or page.endswith("/"):
        page += "index"

    try:
        return render_template(f"pages/{page}.html")
    except TemplateNotFound:
        abort(404)
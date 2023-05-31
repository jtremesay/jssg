from flask import (
    Blueprint, render_template
)

bp = Blueprint('page', __name__)

@bp.route("/<page>")
def page(page:str=""):
    if not page or page.endswith("/"):
        page += "index"

    return render_template(f"pages/{page}.html")
from flask import (
    Blueprint, render_template
)

bp = Blueprint('blog', __name__)

@bp.route("/")
def index():
    return render_template(f"blog/index.html")

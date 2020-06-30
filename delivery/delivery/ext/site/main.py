from flask import request, render_template
from flask import Blueprint

bp = Blueprint("site", __name__)


@bp.route("/")
def index():

    return render_template(
        "index.html",
        name=request.args['name']
    )

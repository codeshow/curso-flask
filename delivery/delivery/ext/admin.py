from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from delivery.ext.db import db
from delivery.ext.db.models import Category

admin = Admin()


def init_app(app):
    admin.name = "CodeFoods"
    admin.template_mode = "bootstrap2"
    admin.init_app(app)

    # TODO: Proteger com senha
    # TODO: traduzir para PTBR

    admin.add_view(ModelView(Category, db.session))

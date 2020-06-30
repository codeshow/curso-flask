from flask import Flask

from delivery.ext import site


def create_app():
    app = Flask(__name__)
    # HEllo
    site.init_app(app)
    return app

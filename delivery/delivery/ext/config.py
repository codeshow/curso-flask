from dynaconf import FlaskDynaconf


def init_app(app):
    FlaskDynaconf(app)
    app.config.load_extensions("EXTENSIONS")

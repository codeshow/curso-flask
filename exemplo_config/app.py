from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('application.cfg')


@app.route("/")
def index():
    return f"CodeShow {app.config['FOO']}"

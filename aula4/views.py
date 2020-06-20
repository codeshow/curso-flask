from app import app


@app.route("/")
def index():
    return "Hello Codeshow"


@app.route("/contato")
def contato():
    return "<form><input type='text'></input></form>"

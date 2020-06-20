"""Extensão Flask"""
from flask import Flask, request


def init_app(app: Flask):
    """Inicialização de extensões"""

    @app.route("/")
    def index():
        print(request.args)
        return "Esta rodando aguarde"

    @app.route("/contato")
    def contato():
        return "<form><input type='text'></input></form>"

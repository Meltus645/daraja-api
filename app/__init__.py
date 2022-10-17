from flask import Flask
from .utils.constants import BASEDIR
from .routes import daraja, public


def create_app():
    app =Flask(__name__)
    app.config.from_pyfile(BASEDIR / 'config.py')

    app.register_blueprint(public, url_prefix ='/')
    app.register_blueprint(daraja, url_prefix ='/daraja')

    return app
# -*- coding: utf-8 -*-
from flask import Flask, request, session, render_template, flash, abort
from flask.ext.babel import Babel
from flask.ext.socketio import SocketIO
import importlib

socketio = SocketIO()
babel = None

def create_app():
    """Create an application."""
    app = Flask(__name__)
    app.config.from_object('flaskberry.settings')
    load_modules(app)

    socketio.init_app(app)

    babel = Babel(app)
    babel.locale_selector_func = get_locale
    return app

def load_modules(app):
    # start page
    from flaskberry.views.main import mod as main_blueprint
    app.register_blueprint(main_blueprint)

    # load and register enabled modules
    for mod_name in app.config['ENABLED_MODULES']:
        module = importlib.import_module('flaskberry.views.'+mod_name)
        app.register_blueprint(module.mod, url_prefix='/'+mod_name)

def get_locale():
    return request.accept_languages.best_match(['en', 'de'])

app = create_app()

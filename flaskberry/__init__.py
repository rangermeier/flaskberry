# -*- coding: utf-8 -*-
from flask import Flask, request, session, render_template, flash, abort
from flask.ext.babel import Babel
import importlib

app = Flask(__name__)
app.config.from_object('flaskberry.settings')
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'de'])


# load and register enabled modules
for mod_name in app.config['ENABLED_MODULES']:
    module = importlib.import_module('flaskberry.views.'+mod_name)
    app.register_blueprint(module.mod, url_prefix='/'+mod_name)


@app.route('/')
def index():
    return render_template('index.html')

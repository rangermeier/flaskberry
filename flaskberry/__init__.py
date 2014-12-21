# -*- coding: utf-8 -*-
from flask import Flask, request, session, render_template, flash, abort
from flask.ext.babel import Babel

app = Flask(__name__)
app.config.from_object('flaskberry.settings')
babel = Babel(app)

from flaskberry.views import system, disks, movies

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(["en", "de"])

app.register_blueprint(system.mod, url_prefix='/system')
app.register_blueprint(disks.mod, url_prefix='/disks')
app.register_blueprint(movies.mod, url_prefix='/movies')

@app.route('/')
def index():
    return render_template('index.html')

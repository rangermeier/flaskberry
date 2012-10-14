# -*- coding: utf-8 -*-
from flask import Flask, request, session, render_template, flash, abort

app = Flask(__name__)
app.config.from_object('flaskberry.settings')

from flaskberry.views import system, disks

app.register_blueprint(system.mod, url_prefix='/system')
app.register_blueprint(disks.mod, url_prefix='/disks')

@app.route('/')
def index():
    return render_template('index.html')

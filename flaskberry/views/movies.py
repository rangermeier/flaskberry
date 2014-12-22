# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, flash, current_app, url_for
from werkzeug.contrib.cache import SimpleCache
import fnmatch
import os
from flask.ext.babel import gettext

mod = Blueprint('movies', __name__)

cache = SimpleCache()

@mod.route('/')
def index():
    if not os.path.isdir(current_app.config['MOVIES_DIR']):
        flash(gettext("Directory %(directory)s not found", directory = directory))
        return redirect("/")

    html = cache.get("movies-html")

    if html is None:
        html = render_template('movies/movies.html', movies=find_movies())
        cache.set('movies-html', html, timeout=7 * 24 * 60 * 60)

    return html


@mod.route('/refresh')
def refresh():
    cache.set('movies-html', None, timeout=7 * 24 * 60 * 60)
    return redirect(url_for('.index'))


def find_movies():
    directory = current_app.config['MOVIES_DIR']
    extensions = current_app.config['MOVIES_EXT']

    movies = {}
    rootPathLen = len(directory)

    for root, dirnames, filenames in os.walk(directory, followlinks=True):
        for filename in filenames:
            u_filename = unicode(filename, 'utf-8')
            u_root = unicode(root, 'utf-8')
            if u_filename.lower().endswith(extensions):
                firstChar = u_filename[0].upper()

                if not firstChar in movies.keys():
                    movies[firstChar] = []

                movies[firstChar].append({
                    'path': os.path.join(u_root, u_filename)[rootPathLen:],
                    'name': u_filename
                })

    return movies    

# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, current_app, url_for, session
from werkzeug.contrib.cache import SimpleCache
import os
from flask.ext.babel import gettext
from . import mod

cache = SimpleCache()

@mod.route('/')
def index():
    if not os.path.isdir(current_app.config['MOVIES_DIR']):
        flash(gettext("Directory %(directory)s not found", directory=directory))
        return redirect("/")

    return render_template('movies/movies.html', movies=get_movies())

@mod.route('/refresh')
def refresh():
    cache.set('movies', None, timeout=7 * 24 * 60 * 60)
    return redirect(url_for('.index'))

@mod.route('/player')
def player():
    return render_template('movies/player.html')

@mod.route('/control')
def control():
    return render_template('movies/control.html', movies=get_movies())


def get_movies():
    movies = cache.get("movies")

    if movies is None:
        movies = find_movies()
        cache.set('movies', movies, timeout=7 * 24 * 60 * 60)

    return movies

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

# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, flash, current_app
import fnmatch
import os
from flask.ext.babel import gettext

mod = Blueprint('movies', __name__)

@mod.route('/')
def index():
    directory = current_app.config['MOVIES_DIR']
    extensions = current_app.config['MOVIES_EXT']

    if not os.path.isdir(directory):
        flash(gettext("Directory %(directory)s not found", directory = directory))
        return redirect("/")

    movies = {}
    rootPathLen = len(directory)

    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            u_filename = unicode(filename, 'utf-8')
            if u_filename.lower().endswith(extensions):
                firstChar = u_filename[0].upper()

                if not firstChar in movies.keys():
                    movies[firstChar] = []
                movies[firstChar].append({
                    'path': os.path.join(root, u_filename)[rootPathLen:],
                    'name': u_filename
                })

    return render_template('movies/movies.html', movies=movies)

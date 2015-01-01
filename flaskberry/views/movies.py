# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, flash, current_app, url_for, session
from werkzeug.contrib.cache import SimpleCache
import fnmatch
import os
from flask.ext.babel import gettext
from flask.ext.socketio import send, emit, join_room, leave_room
from .. import socketio

mod = Blueprint('movies', __name__)

cache = SimpleCache()

status = {
    'consumers': 0
}

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

@socketio.on('register consumer', namespace='/movies/player')
def socket_register_player(data):
    status['consumers'] += 1
    join_room('consumers')
    session["is_player"] = True
    emit('play', status)
    emit_status()

@socketio.on('register controller', namespace='/movies/player')
def socket_register_player(data):
    emit_status()

@socketio.on('disconnect', namespace='/movies/player')
def socket_disconnect():
    if session.get('is_player'):
        status['consumers'] = max(0, status['consumers'] - 1)
        emit_status()

@socketio.on('play', namespace='/movies/player')
def socket_play(data):
    emit('play', data, room='consumers')

@socketio.on('update status', namespace='/movies/player')
def socket_status(data):
    fields = ["src", "paused", "currentTime", "duration", "volume", "muted", "fullscreen"]
    for field in data.keys():
        if data.has_key(field):
            status[field] = data[field]
    emit_status()

def emit_status():
    emit('status', status, broadcast=True)


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

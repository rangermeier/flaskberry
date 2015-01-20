# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, current_app, url_for, session, jsonify, request, Response
from flask.ext.babel import gettext
from werkzeug.contrib.cache import SimpleCache
import os
import urllib
import gzip
import requests
import StringIO
import re
import xmlrpclib
from os_util import OSFile
from . import mod

cache = SimpleCache()

OST_API = 'http://api.opensubtitles.org/xml-rpc'
OST_USERAGENT = 'Flaskberry'

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


@mod.route('/subtitles')
def find_subtitles():
    rel_path = request.args.get('src')[len(current_app.config["MOVIES_URL"])+1:]
    json = cache.get(rel_path)
    if json == None:
        path = os.path.join(
                current_app.config['MOVIES_DIR'],
                urllib.unquote(rel_path).decode('utf8')
            )

        subtitles = []
        results = os_search(path)
        try:
            for sub in results:
                if sub['SubFormat'] == 'srt':
                    subtitles.append({
                        'url': sub['SubDownloadLink'],
                        'language': sub['LanguageName'],
                        'name': sub['MovieName']
                    })
        except TypeError:
            pass
        json = jsonify(
            subtitles=subtitles
        )
        cache.set(rel_path, json, timeout=7 * 24 * 60 * 60)
    return json

@mod.route("/subtitleproxy")
def subtitle_proxy():
    src = request.args.get('src')
    vtt = cache.get(src)
    if vtt == None:
        r = requests.get(src)
        gzipped = StringIO.StringIO(r.content)
        gzipped.seek(0)
        srt = gzip.GzipFile(fileobj=gzipped, mode='rb')
        vtt = srt_to_vtt(srt.read())
        cache.set(src, vtt, timeout=7 * 24 * 60 * 60)
    return Response(vtt, mimetype='text/vtt')

def os_search(path):
    xmlrpc, token = os_connect()
    xmlrpclib.Marshaller.dispatch[type(0L)] = lambda _, v, w: w("<value><i8>%d</i8></value>" % v)

    # try searching by file hash
    os_file = OSFile(path)
    query = xmlrpc.SearchSubtitles(token, [
            {
                'sublanguageid': current_app.config['MOVIES_OS_LANG'],
                'moviehash': os_file.hash_file(),
                'moviebytesize': os_file.size,

            }
        ])
    if len(query.get('data')) > 0:
        return query.get('data')

    # fallback searching by file name
    filename = os.path.splitext(os.path.basename(path))[0].replace(".", " ")
    query = xmlrpc.SearchSubtitles(token, [
            {
                'sublanguageid': current_app.config['MOVIES_OS_LANG'],
                'query': filename,

            }
        ])
    return query.get('data')


def os_connect():
    xmlrpc = xmlrpclib.ServerProxy(OST_API, allow_none=True)
    login = xmlrpc.LogIn(
        current_app.config['MOVIES_OS_USER'],
        current_app.config['MOVIES_OS_PASSWORD'],
        "en",
        OST_USERAGENT
    )

    if login.get('status') == '200 OK':
        return (xmlrpc, login.get('token'))

def srt_to_vtt(srt):
    vtt = "WEBVTT\n\n"
    vtt += re.sub(r'([0-9]{2}:[0-9]{2}:[0-9]{2}),([0-9]{3})', r'\1.\2', srt)
    return vtt


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

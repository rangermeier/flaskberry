# -*- coding: utf-8 -*-
from flask import session
from flask.ext.socketio import send, emit, join_room
from ... import socketio

status = {
    'consumers': 0
}
namespace = '/movies/player'

@socketio.on('register consumer', namespace=namespace)
def socket_register_player(data):
    status['consumers'] += 1
    join_room('consumers')
    session["is_player"] = True
    emit('play', status)
    emit_status()

@socketio.on('register controller', namespace=namespace)
def socket_register_player(data):
    emit_status()

@socketio.on('disconnect', namespace=namespace)
def socket_disconnect():
    if session.get('is_player'):
        status['consumers'] = max(0, status['consumers'] - 1)
        emit_status()

@socketio.on('play', namespace=namespace)
def socket_play(data):
    emit('play', data, room='consumers')

@socketio.on('update status', namespace=namespace)
def socket_status(data):
    fields = ["src", "paused", "currentTime", "duration", "volume", "muted", "fullscreen"]
    for field in data.keys():
        if data.has_key(field):
            status[field] = data[field]
    emit_status()

def emit_status():
    emit('status', status, broadcast=True)

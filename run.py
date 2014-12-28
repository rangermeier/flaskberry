# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from flaskberry import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app)

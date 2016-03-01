#!/usr/bin/env python

from gevent.wsgi import WSGIServer
from geventwebsocket import WebSocketServer, WebSocketError
from geventwebsocket.handler import WebSocketHandler
from twidder import app
from multiprocessing import Process

# ------------

if __name__ == '__main__':
    server = WebSocketServer(("", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

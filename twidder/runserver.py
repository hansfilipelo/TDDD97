#!/usr/bin/env python

from gevent.wsgi import WSGIServer
from geventwebsocket import WebSocketServer, Resource
from twidder import app
from multiprocessing import Process
from twidder.websocket import InactiveEnabler

def http_server(port):
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()

# ------------

def ws_server(port):
    WebSocketServer(('', port),Resource({'/': InactiveEnabler})).serve_forever()

# ------------

http = Process(target=http_server, args=(5000,))
wsocket = Process(target=ws_server, args=(8000,))

http.start()
wsocket.start()

http.join()
wsocket.join()

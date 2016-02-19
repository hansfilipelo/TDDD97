#!/usr/bin/env python

from flask import Flask
import database_helper
from flask import g

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/sign_in")
def sign_in(email, password):
  return


# Teardown of app

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

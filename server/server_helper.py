#!/usr/bin/env python

from flask import Flask
from flask import request
import db
from flask import g
import hashlib, uuid
import random

_USER_TOKEN_MIN_ = 1000
_USER_TOKEN_MAX_ = 100000

app = Flask(__name__)
app.debug = True

signed_in_users = {}

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/sign_in")
def sign_in():
    email = request.args.get('email')
    password = request.args.get('password')

    userInfo = db.query_db('select * from users where email=?', [email], one=True)

    if userInfo != None:
        if hashlib.sha512(password + userInfo["salt"]).hexdigest() == userInfo["passwordHash"]:
            random.seed()
            token = str(random.randint(_USER_TOKEN_MIN_,_USER_TOKEN_MAX_))
            while token in signed_in_users.keys():
                token = str(random.randint(_USER_TOKEN_MIN_,_USER_TOKEN_MAX_))

            signed_in_users[token] = email
            return token
    else:
        return 'OK'

@app.route("/sign_up")
def sign_up(email, password, firstname, familyname, gender, city, country):
    return


# Teardown of app

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

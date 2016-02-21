#!/usr/bin/env python

from flask import Flask
from flask import request
from db import *
from flask import g
import hashlib, uuid
import random

_USER_TOKEN_MIN_ = 1000
_USER_TOKEN_MAX_ = 100000
_SALT_MIN_ = 100000
_SALT_MAX_ = 10000000

app = Flask(__name__)
app.debug = True

signed_in_users = {}

@app.route("/")
def hello():
  return "Hello World!"

# ----------------------------

@app.route("/sign_in")
def sign_in():
    email = request.args.get('email')
    password = request.args.get('password')

    userInfo = query_db('select * from users where email=?', [email], one=True)

    if userInfo != None:
        if hashlib.sha512(password + userInfo["salt"]).hexdigest() == userInfo["passwordHash"]:
            random.seed()
            token = str(random.randint(_USER_TOKEN_MIN_,_USER_TOKEN_MAX_))
            while token in signed_in_users.keys():
                token = str(random.randint(_USER_TOKEN_MIN_,_USER_TOKEN_MAX_))

            signed_in_users[token] = email
            return token
        else:
            return 'Wrong password.'
    else:
        return 'No user with that username.'

# ----------------------------

@app.route("/sign_up")
def sign_up():
    email = request.args.get('email')
    password = request.args.get('password')
    firstname = request.args.get('firstname')
    familyName = request.args.get('familyname')

    gender = request.args.get('gender')
    if gender == "male":
        gender = 0
    elif gender == "female":
        gender = female

    city = request.args.get('city')
    country = request.args.get('country')
    salt = random.randint(_SALT_MIN_, _SALT_MAX_)

    if query_db('select * from users where email=?', [email], one=True) == None:
        db_country = query_db('select * from countries where name=?', [country], one=True)
        db_city = None

        if db_country == None:
            query_db('INSERT INTO countries(name) VALUES(?)', [country])
            db_country = query_db('select * from countries where name=?', [country], one=True)
            query_db('INSERT INTO cities(name, country) VALUES(?,?)', [city,db_country["idcountries"]])
            db_city = query_db('select * from cities where name=? AND country=?', [city, db_country["idcountries"]], one=True)
        elif db_city == None:
            query_db('INSERT INTO cities(name, country) VALUES(?,?)', [city,db_country["idcountries"]])
            db_city = query_db('select * from cities where name=? AND country=?', [city, db_country["idcountries"]], one=True)

        query_db('INSERT INTO users(email, passwordHash, firstname, familyName, gender, city, salt) VALUES(?,?,?,?,?,?,?)', [email, hashlib.sha512(password + str(salt)).hexdigest(), firstname, familyName, gender, db_city["idcities"], str(salt)])
        return 'Sign up ok'
    else:
        return 'User already exists.'



# Teardown of app

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

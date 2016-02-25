#!/usr/bin/env python
from __future__ import print_function
from flask import Flask
from flask import request
from db import *
from flask import g
import hashlib, uuid
import random
import json
import sys

_USER_TOKEN_MIN_ = 1000
_USER_TOKEN_MAX_ = 100000
_SALT_MIN_ = 100000
_SALT_MAX_ = 10000000

app = Flask(__name__)
app.debug = True

signed_in_users = {}
user_data_keys = ["email", "firstname", "familyname", "gender", "city", "country"]

@app.route("/")
def hello():
  return "Hello World!"

# ----------------------------

def hash_password(password, salt):
    return hashlib.sha512(password + salt).hexdigest()

def get_email_from_token(token):
    return signed_in_users[token]

# ----------------------------

@app.route("/sign_in")
def sign_in():
    email = request.headers.get('email')
    password = request.headers.get('password')

    userInfo = query_db('select email,passwordHash,salt from users where email=?', [email], one=True)

    if userInfo != None:
        if hash_password(password, userInfo[2]) == userInfo[1]:
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
    email = request.headers.get('email')
    password = request.headers.get('password')
    firstname = request.headers.get('firstname')
    familyName = request.headers.get('familyname')

    gender = request.headers.get('gender')
    if gender == "male":
        gender = 0
    elif gender == "female":
        gender = female

    city = request.headers.get('city')
    country = request.headers.get('country')
    salt = str(random.randint(_SALT_MIN_, _SALT_MAX_))

    if query_db('select * from users where email=?', [email], one=True) == None:
        db_country = query_db('select * from countries where name=?', [country], one=True)[0]
        db_city = None
        try:
            db_city = query_db('SELECT * FROM cities WHERE name=? AND country=?', [city, db_country["idcountries"]], one=True)[0]
        except TypeError:
            pass


        if db_country == None:
            query_db('INSERT INTO countries(name) VALUES(?)', [country])
            db_country = query_db('select * from countries where name=?', [country], one=True)[0]
            query_db('INSERT INTO cities(name, country) VALUES(?,?)', [city,db_country["idcountries"]])
            db_city = query_db('select * from cities where name=? AND country=?', [city, db_country["idcountries"]], one=True)[0]
        elif db_city == None:
            query_db('INSERT INTO cities(name, country) VALUES(?,?)', [city,db_country["idcountries"]])
            db_city = query_db('select * from cities where name=? AND country=?', [city, db_country["idcountries"]], one=True)[0]

        query_db('INSERT INTO users(email, passwordHash, firstname, familyName, gender, city, salt) VALUES(?,?,?,?,?,?,?)', [email, hash_password(password, salt), firstname, familyName, gender, db_city["idcities"], salt])
        return 'Sign up ok'
    else:
        return 'User already exists.'

# ----------------------------
@app.route("/sign_out")
def sign_out():
    token = request.headers.get('token')

    if token in signed_in_users:
        del signed_in_users[token]
    return "Signed out"

# ----------------------------
@app.route("/change_password")
def change_password():
    token = request.headers.get('token')
    old_password = request.headers.get('old_password')
    new_password = request.headers.get('new_password')
    salt = str(random.randint(_SALT_MIN_, _SALT_MAX_))

    userInfo = get_user_info(get_email_from_token(token))

    if userInfo != None:
        if hash_password(old_password, userInfo["salt"]) == userInfo["passwordHash"]:
            query_db('UPDATE users SET passwordHash=?, salt=? WHERE email=?', [hash_password(new_password,salt), salt, signed_in_users[token]])
            return "Updated password"
        print(userInfo["passwordHash"])
        print(hash_password(old_password, userInfo["salt"]))
        return "Incorrect old password"
    return "User not signed in"

# ----------------------------

@app.route("/usermessages")
def get_user_messages_by_token():
    token = request.headers.get('token')
    email = get_email_from_token(token)
    return_data = dict()

    if token in signed_in_users:
        from_users = []
        to_users = []
        content = []
        query = query_db('SELECT fromUser,toUser,content FROM messages WHERE toUser=(SELECT idusers FROM users WHERE email=?)', [email])
        for row in query:
            from_users.append(query_db('SELECT email FROM users WHERE idusers=?', [row[0]], one=True)[0])
            to_users.append(query_db('SELECT email FROM users WHERE idusers=?', [row[1]], one=True)[0])
            content.append(row[2])


        return_data["content"] = []
        return_data["from_user"] = []
        return_data["to_user"] = []
        for i in range(0, len(query)):
            return_data["content"].append(content[i])
            return_data["from_user"].append(from_users[i])
            return_data["to_user"].append(to_users[i])

        return json.dumps({"success": "true", "message": "OK", "data": return_data})

    return json.dumps({"success": "false", "message": "User not signed in."})

# ----------------------------

@app.route("/usermessages/<email>")
def get_user_messages_by_email(email):
    token = request.headers.get('token')
    return_data = dict()

    if token in signed_in_users:
        from_users = []
        to_users = []
        content = []
        query = query_db('SELECT fromUser,toUser,content FROM messages WHERE toUser=(SELECT idusers FROM users WHERE email=?)', [email])
        for row in query:
            from_users.append(query_db('SELECT email FROM users WHERE idusers=?', [row[0]], one=True)[0])
            to_users.append(query_db('SELECT email FROM users WHERE idusers=?', [row[1]], one=True)[0])
            content.append(row[2])


        return_data["content"] = []
        return_data["from_user"] = []
        return_data["to_user"] = []
        for i in range(0, len(query)):
            return_data["content"].append(content[i])
            return_data["from_user"].append(from_users[i])
            return_data["to_user"].append(to_users[i])

        return json.dumps({"success": "true", "message": "OK", "data": return_data})

    return json.dumps({"success": "false", "message": "User not signed in."})

# ----------------------------
@app.route("/userdata/<email>")
def get_user_data_by_email(email):
    token = request.headers.get('token')

    if token in signed_in_users:
        user_info = get_user_info(email)
        return json.dumps({"success": "true", "message": "Success!", "data": dict_from_query(query)})

    return json.dumps({"success": "false", "message": "User not signed in."})

# ----------------------------

@app.route("/userdata")
def get_user_data_by_token():
    token = request.headers.get('token')
    email = get_email_from_token(token)

    if token in signed_in_users:
        user_info = get_user_info(email)
        return json.dumps({"success": "true", "message": "Success!", "data": dict_from_query(query)})

    return json.dumps({"success": "false", "message": "User not signed in."})

# ----------------------------
@app.route("/post_message/<email>")
def post_message(email):
    token = request.headers.get('token')
    message = request.headers.get('message')

    if token in signed_in_users:
        from_id = query_db('SELECT idusers FROM users WHERE email=?', [get_email_from_token(token)], one=True)[0]
        to_id = query_db('SELECT idusers FROM users WHERE email=?', [email], one=True)[0]
        query_db('INSERT INTO messages(fromUser, toUser, content) VALUES(?,?,?)', [from_id, to_id, message])
        return json.dumps({"success": "true", "message": "Posted message."})

    return json.dumps({"success": "false", "message": "User not signed in."})

# Teardown of app

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

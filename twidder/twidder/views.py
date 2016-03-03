#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, request, render_template
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

from twidder import app

signed_in_users = {}

@app.route("/")
def index():
    return app.send_static_file("client.html")

# ----------------------------

def hash_password(password, salt):
    return hashlib.sha512(password + salt).hexdigest()

def get_email_from_token(token):
    return signed_in_users[token]

# ----------------------------

@app.route("/sign_in", methods=['GET', 'POST'])
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
            return json.dumps({"success": True, "message": "Sign in OK", "data": token})
        else:
            return json.dumps({"success": False, "message": "Wrong password."})
    else:
        return json.dumps({"success": False, "message": "No user with that username."})

# ----------------------------

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    email = request.headers.get('email')
    password = request.headers.get('password')
    firstname = request.headers.get('firstname')
    familyName = request.headers.get('familyname')

    gender = request.headers.get('gender')
    if gender == "male":
        gender = 0
    else:
        gender = 1

    city = request.headers.get('city')
    country = request.headers.get('country')
    salt = str(random.randint(_SALT_MIN_, _SALT_MAX_))

    if query_db('select * from users where email=?', [email], one=True) == None:
        db_country = query_db('select name,idcountries from countries where name=?', [country], one=True)
        db_city = None
        try:
            db_city = query_db('SELECT * FROM cities WHERE name=? AND country=?', [city, db_country[1]], one=True)[0]
        except TypeError:
            pass


        if db_country == None:
            query_db('INSERT INTO countries(name) VALUES(?)', [country])
            db_country = query_db('select name,idcountries from countries where name=?', [country], one=True)
            query_db('INSERT INTO cities(name, country) VALUES(?,?)', [city,db_country[1]])
            db_city = query_db('select idcities from cities where name=? AND country=?', [city, db_country[1]], one=True)
        elif db_city == None:
            query_db('INSERT INTO cities(name, country) VALUES(?,?)', [city,db_country[1]])
            db_city = query_db('select idcities from cities where name=? AND country=?', [city, db_country[1]], one=True)

        query_db('INSERT INTO users(email, passwordHash, firstname, familyName, gender, city, salt) VALUES(?,?,?,?,?,?,?)', [email, hash_password(password, salt), firstname, familyName, gender, db_city, salt])
        return json.dumps({"success": True, "message": "Sign up OK!"})
    else:
        return json.dumps({"success": false, "message": "User already exists."})

# ----------------------------
@app.route("/sign_out", methods=['GET', 'POST'])
def sign_out():
    token = request.headers.get('token')

    if token in signed_in_users:
        del signed_in_users[token]
        return json.dumps({"success": True, "message": "Signed out."})

    return json.dumps({"success": False, "message": "User not signed in."})

# ----------------------------
def get_user_messages_helper(token, to_email):
    return_data = dict()

    if token in signed_in_users:
        from_users = []
        to_users = []
        content = []
        query = query_db('SELECT fromUser,toUser,content FROM messages WHERE toUser=(SELECT idusers FROM users WHERE email=?)', [to_email])
        for row in query:
            from_users.append(query_db('SELECT email FROM users WHERE idusers=?', [row[0]], one=True)[0])
            to_users.append(query_db('SELECT email FROM users WHERE idusers=?', [row[1]], one=True)[0])
            content.append(row[2])


        return_data["content"] = []
        return_data["writer"] = []
        return_data["to_user"] = []
        for i in range(0, len(query)):
            return_data["content"].append(content[i])
            return_data["writer"].append(from_users[i])
            return_data["to_user"].append(to_users[i])

        return json.dumps({"success": True, "message": "OK", "data": return_data})

    return json.dumps({"success": False, "message": "User not signed in."})

# ----------------------------

@app.route("/usermessages", methods=['GET', 'POST'])
def get_user_messages_by_token():
    token = request.headers.get('token')
    to_email = get_email_from_token(token)

    return get_user_messages_helper(token, to_email)


# ----------------------------

@app.route("/usermessages/<to_email>", methods=['GET', 'POST'])
def get_user_messages_by_email(to_email):
    token = request.headers.get('token')

    return get_user_messages_helper(token, to_email)

# ----------------------------

def get_user_data_helper(token, email):
    if token in signed_in_users:
        user_info = query_db('SELECT email,firstname,familyName,gender,city FROM users WHERE email=?', [email], one=True)
        city_info = query_db('SELECT name,country FROM cities WHERE idcities=?', [user_info[4]], one=True)
        country_info = query_db('SELECT name FROM countries WHERE idcountries=?', [city_info[1]], one=True)

        return_data = dict()
        return_data["email"] = user_info[0]
        return_data["firstname"] = user_info[1]
        return_data["familyname"] = user_info[2]
        if user_info[3] == 0:
            return_data["gender"] = "male"
        else:
            return_data["gender"] = "female"
        return_data["city"] = city_info[0]
        return_data["country"] = country_info[0]

        return json.dumps({"success": True, "message": "Success!", "data": return_data})

    return json.dumps({"success": False, "message": "User not signed in."})


@app.route("/userdata/<email>", methods=['GET', 'POST'])
def get_user_data_by_email(email):
    token = request.headers.get('token')
    return get_user_data_helper(token, email)

# ----------------------------

@app.route("/userdata", methods=['GET', 'POST'])
def get_user_data_by_token():
    token = request.headers.get('token')
    email = get_email_from_token(token)

    return get_user_data_helper(token, email)

# ----------------------------
@app.route("/post_message/<email>", methods=['GET', 'POST'])
def post_message(email):
    token = request.headers.get('token')
    message = request.headers.get('content')

    if token in signed_in_users:

        from_id = query_db('SELECT idusers FROM users WHERE email=?', [get_email_from_token(token)], one=True)[0]
        to_id = 0
        temp_to = query_db('SELECT idusers FROM users WHERE email=?', [email], one=True)
        if temp_to:
            to_id = temp_to[0]

        query_db('INSERT INTO messages(fromUser, toUser, content) VALUES(?,?,?)', [from_id, to_id, message])
        return json.dumps({"success": True, "message": "Posted message."})

    return json.dumps({"success": False, "message": "User not signed in."})

# ----------------------------
@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    token = request.headers.get('token')
    old_password = request.headers.get('old_password')
    new_password = request.headers.get('new_password')
    email = get_email_from_token(token)
    salt = str(random.randint(_SALT_MIN_, _SALT_MAX_))

    user_info = query_db('SELECT passwordHash, salt FROM users WHERE email=?', [email], one=True)
    password_hash = user_info[0]
    old_salt = user_info[1]

    if user_info != None:
        if hash_password(old_password, old_salt) == password_hash:
            query_db('UPDATE users SET passwordHash=?, salt=? WHERE email=?', [hash_password(new_password,salt), salt, email])
            return json.dumps({"success": True, "message": "Updated password."})
        return json.dumps({"success": False, "message": "Incorrect old password"})
    return json.dumps({"success": False, "message": "User not signed in"})

# Teardown of app

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

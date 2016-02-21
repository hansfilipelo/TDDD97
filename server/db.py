#!/usr/bin/env python

import sqlite3
from flask import g

_DATABASE_ = 'database.sdb'

# Define nessecary function
def connect_to_database():
    return sqlite3.connect(_DATABASE_)

# Get the DB
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    # Return rows as dictionaries
    db.row_factory = sqlite3.Row
    return db

# Query-DB function which returns dicts
def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    db.commit()
    return (rv[0] if rv else None) if one else rv

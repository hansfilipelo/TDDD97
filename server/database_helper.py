#!/usr/bin/env python

import sqlite3
from flask import g

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = connect_to_database()
  return db
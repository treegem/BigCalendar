import sqlite3

from flask import g


def connect_db(database_location):
    """Connects to the specific database."""
    # rv = sqlite3.connect(app.config['DATABASE'])
    rv = sqlite3.connect(database_location)
    rv.row_factory = sqlite3.Row
    return rv


def get_db(database_location):
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(database_location)
    return g.sqlite_db


def init_db(app):
    db = get_db(app.config['DATABASE'])
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

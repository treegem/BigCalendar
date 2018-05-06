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


def full_user_list(database):
    users = entry_list(prop='user', table='logins', database=database)
    return users


def full_password_list(database):
    passwords = entry_list(prop='password', table='logins', database=database)
    return passwords


def entry_list(prop, table, database):
    db = get_db(database)
    request = db.execute(
        'select {} from {}'.format(prop, table))
    sql_list = request.fetchall()
    entries = []
    for entry in sql_list:
        entries.append(entry[prop])
    return entries


def read_from_app_db(app, properties, table, additional=''):
    joined_properties = ', '.join(properties)
    db = get_db(app.config['DATABASE'])
    cur = db.execute(
        'select {0} from {1}{2}'.format(joined_properties, table, additional))
    return cur.fetchall()

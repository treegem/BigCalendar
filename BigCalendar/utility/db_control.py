import sqlite3

from flask import g

from BigCalendar.utility.db_pre_post_processing import collective_availability, comma_separated_entries


def connect_db(database_location):
    """Connects to the specific database."""
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
    request_ = db.execute(
        'select {} from {}'.format(prop, table))
    sql_list = request_.fetchall()
    entries = []
    for entry in sql_list:
        entries.append(entry[prop])
    return entries


def read_from_app_db(app, properties, table, additional=''):
    joined_properties = comma_separated_entries(properties)
    db = get_db(app.config['DATABASE'])
    cur = db.execute(
        'select {0} from {1}{2}'.format(joined_properties, table, additional))
    return cur.fetchall()


def insert_into_app_db(app, properties, table, values):
    joined_properties = comma_separated_entries(properties)
    placeholder = ['?' for _ in range(len(properties))]
    placeholder = comma_separated_entries(placeholder)
    db = get_db(app.config['DATABASE'])
    db.execute('insert into {0} ({1}) values ({2})'.format(table, joined_properties, placeholder), values)
    db.commit()


def entry_in_app_db(app, table: str, target: dict):
    found = False
    target_str = list(target.keys())[0]
    if target_str not in get_table_column_names(app, table):
        return found
    target_val = list(target.values())[0]
    entries = read_from_app_db(
        app=app,
        properties=[target_str],
        table=table,
    )
    for entry in entries:
        if entry[target_str] == target_val:
            found = True
    return found


def get_table_column_names(app, table):
    db = get_db(app.config['DATABASE'])
    query = db.execute('pragma table_info({})'.format(table)).fetchall()
    column_names = []
    for column in query:
        column_names.append(column[1])
    return column_names


def create_availability_entry(id_, app):
    column_names = get_table_column_names(app, 'availabilities')
    insert_into_app_db(
        app=app,
        properties=[*column_names],
        table='availabilities',
        values=[id_] + [2] * (len(column_names) - 1)
    )


def update_app_db(app, table, property, value, where):
    db = get_db(app.config['DATABASE'])
    db.execute('update {0} set {1} = {2} where {3}'.format(table, property, value, where))
    db.commit()


def update_entries_availability(app, id_number):
    column_names = get_table_column_names(app, 'availabilities')[1:]
    user_availabilities = read_from_app_db(app=app, table='availabilities', properties=column_names,
                                           additional=' where id = {}'.format(id_number))[0]
    id_availability = collective_availability(column_names, user_availabilities)
    update_app_db(app=app, table='entries', property='available', value=id_availability,
                  where='id = {}'.format(id_number))



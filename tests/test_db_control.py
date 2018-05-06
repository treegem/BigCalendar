import os

from BigCalendar.utility.db_control import *
from BigCalendar.big_calendar import app

app.config['DATABASE'] = 'test.db'
database_ = app.config['DATABASE']


def test_db_creation():
    if os.path.isfile(database_):
        os.unlink(database_)
    assert not os.path.isfile(database_)

    with app.app_context():
        init_db(app)
    assert os.path.isfile(database_)


def test_read_from_app_db_empty_read_all():
    with app.app_context():
        entries = read_from_app_db(
            app=app,
            properties=['*'],
            table='entries',
        )
    assert entries == []


def test_insert_into_app_db():
    with app.app_context():
        insert_into_app_db(
            app=app,
            properties=['user', 'password'],
            table='logins',
            values=['user_test', 'password_test']
        )
        logins = read_from_app_db(
            app=app,
            properties=['*'],
            table='logins'
        )
    assert logins[0]['user'] == 'user_test'
    assert logins[0]['password'] == 'password_test'

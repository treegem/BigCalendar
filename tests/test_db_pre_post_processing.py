import os

from BigCalendar.utility.db_pre_post_processing import *
from BigCalendar.utility.db_control import *
from BigCalendar.big_calendar import app

app.config['DATABASE'] = 'test.db'
database_ = app.config['DATABASE']

with app.app_context():
    if os.path.isfile(database_):
        os.unlink(database_)
    init_db(app)
    insert_into_app_db(
        app=app,
        properties=['mic', 'bass', 'drums', 'guitar', 'keys'],
        table='availabilities',
        values=[0, 1, 2, 1, 0]
    )


def test_who_is_unavailable():
    who = who_is_unavailable()
    assert who == 'mic, keys'

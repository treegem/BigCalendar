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

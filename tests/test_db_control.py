import os

from BigCalendar.utility.db_control import *
from BigCalendar.big_calendar import app

app.config['DATABASE'] = 'test.db'


def test_db_creation():

    with app.app_context():
        init_db(app)
    assert os.path.isfile(app.config['DATABASE'])

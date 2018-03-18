import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

from BigCalendar.utility.db_control import get_db, init_db

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'big_calendar.db'),  # TODO: Instance Folders
    DEBUG=True,
    SECRET_KEY='development key',  # TODO
    USERNAME='admin',  # TODO
    PASSWORD='default'  # TODO
))


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db(app)
    print('Initialized the database.')


@app.route('/')
def show_entries():
    add = request.args.get('add')
    db = get_db(app.config['DATABASE'])
    cur = db.execute('select text, concert_date, available from entries order by concert_date asc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries, add=add)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    checkbox = checkbox_to_boolean()
    db = get_db(app.config['DATABASE'])
    db.execute('insert into entries (text, concert_date, available) values (?, ?, ?)',
               [request.form['text'], request.form['date'], checkbox])
    db.commit()
    flash('Neuer Eintrag erfolgreich hinzugefuegt.')
    return redirect(url_for('show_entries'))


@app.route('/add_true')
def add_true():
    return redirect(url_for('show_entries', add=True))


def checkbox_to_boolean():
    if 'checkbox' in request.form:
        checkbox = True
    else:
        checkbox = False
    return checkbox


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

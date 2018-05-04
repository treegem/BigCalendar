import os

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

from BigCalendar.utility.db_control import get_db, init_db, full_user_list, full_password_list
from BigCalendar.utility.id_handling import opposite_id
from BigCalendar.utility.encryption import encrypt_sha256

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'big_calendar.db'),  # TODO: Instance Folders
    DEBUG=True,
    SECRET_KEY='development key',  # TODO
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
    cur = db.execute(
        'select id, text, concert_date, available from entries order by concert_date asc')  # TODO: join with availability
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries, add=add)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    checkbox = 1  # TODO: remove
    db = get_db(app.config['DATABASE'])
    db.execute('insert into entries (text, concert_date, available) values (?, ?, ?)',
               # TODO: available separated into availability
               [request.form['text'], request.form['date'], checkbox])
    db.commit()
    flash('Neuer Eintrag erfolgreich hinzugefuegt.')
    return redirect(url_for('show_entries'))


@app.route('/add_true')
def add_true():
    return redirect(url_for('show_entries', add=True))


@app.route('/login', methods=['GET', 'POST'])
def login():
    database = app.config['DATABASE']
    error = None
    if request.method == 'POST':
        if request.form['username'] not in full_user_list(database):
            error = 'Invalid username'
        elif encrypt_sha256(request.form['password']) not in full_password_list(database):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['user'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/checkbox_clicked/<id>', methods=['GET', 'POST'])
def checkbox_clicked(id_):
    other_id = opposite_id(id_)
    return jsonify(other_id=other_id, id=id_)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

import os

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

from BigCalendar.utility.db_control import get_db, init_db, full_user_list, full_password_list, read_from_app_db
from BigCalendar.utility.id_handling import opposite_id, split_id
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
    entries = read_from_app_db(
        app=app,
        properties=['id', 'text', 'concert_date', 'available'],
        table='entries',
        additional=' order by concert_date asc'
    )
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
    error = None
    if request.method == 'POST':
        database = app.config['DATABASE']
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


def bool_conversion(checked):
    if checked == 'true' or checked is True:
        return True
    elif checked == 'false' or checked is False:
        return False


@app.route('/checkbox_clicked/<id_>/<checked>', methods=['GET', 'POST'])
def checkbox_clicked(id_, checked):
    available = availability(id_, checked)
    other_id = opposite_id(id_)
    return jsonify(other_id=other_id, id=id_)


def availability(id_, checked):
    checked = bool_conversion(checked)
    id_category = split_id(id_)[0]
    if (id_category == 'yes' and checked) or (id_category == 'no' and not checked):
        available = True
    elif (id_category == 'yes' and not checked) or (id_category == 'no' and checked):
        available = False
    return available


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

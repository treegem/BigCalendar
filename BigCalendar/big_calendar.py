import os

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

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
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['user'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/checkbox_clicked/<id>', methods=['GET', 'POST'])
def checkbox_clicked(id):
    other_id = opposite_id(id)
    return jsonify(other_id=other_id, id=id)


def opposite_id(id):
    split_id = id.split('_')
    this_id_category = split_id[0]
    this_id_number = split_id[1]
    other_id_category = opposite_id_category(this_id_category)
    other_id = '_'.join([other_id_category, this_id_number])
    return other_id


def opposite_id_category(this_id_category):
    if this_id_category == 'yes':
        other_id_category = 'no'
    elif this_id_category == 'no':
        other_id_category = 'yes'
    return other_id_category


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

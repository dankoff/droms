import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
from app.util import get_work_places
from app.index import freeSeat

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    ''' View func for registering a new user '''
    if not g.user:
        return redirect(url_for('auth.login'))
    elif g.user['type'] != 'Manager':
        return redirect(url_for('kitchen.home'))
    work_places = get_work_places()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confPass = request.form.get('confPassword')
        staffType = request.form.get('staffType')
        workPlace = request.form.get('workPlace')

        db = get_db()
        error = None

        if (len(password) < 6):
            error = 'Password must be at least 6 characters long.'
        elif (password != confPass):
            error = 'Passwords must match.'
        elif db.execute(
            'SELECT id FROM staff WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'Staff with username {} is already registered'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO staff (username, password, type, workPlace)'
                ' VALUES (?,?,?,?)',
                (username, generate_password_hash(password), staffType, workPlace)
            )
            db.commit()
            return redirect(url_for('kitchen.home'))

        flash(error)
    return render_template('auth/register.html', work_places=work_places)

@bp.route('/login', methods=['GET','POST'])
def login():
    """ View func for logging in a user """
    if g.user:
        return redirect(url_for('kitchen.home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT id, username, password, type FROM staff WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.pop('user_id', None)
            session['user_id'] = user['id']
            # free seat if user successfully logs in
            if 'tableNo' in session:
                freeSeat(session['tableNo'])
            return redirect(url_for('kitchen.home'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM staff WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('.login'))

def login_required(types=None):
    def wrapper(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))
            else:
                if types:
                    if g.user['type'] not in types:
                        return redirect(url_for('menu.index'))

            return view(**kwargs)
        return wrapped_view
    return wrapper

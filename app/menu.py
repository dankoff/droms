from flask import (
    Blueprint, request, redirect, url_for, flash, render_template
)

from werkzeug.exceptions import abort
from app.db import get_db

bp = Blueprint('menu', __name__)

@bp.route('/')
def index():
    db = get_db()
    items = db.execute(
        'SELECT * FROM item ORDER BY name ASC'
    ).fetchall()
    return render_template('index.html', items=items)

@bp.route('/add_section', methods=('GET', 'POST'))
def add_section():
    ''' adds a new menu section '''
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        error = None

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO section (name, description, menu)'
                ' VALUES (?,?,"Main Menu")',
                (name, desc)
            )
            db.commit()
            return redirect( url_for('menu.index') )
    return render_template( 'add_section.html' )

@bp.route('/add_item', methods=('GET', 'POST'))
def add_item():
    ''' adds a new menu item to the database '''
    sections = get_all_sections()
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        cost = request.form['cost']
        section = request.form['section']
        error = None

        if not name:
            error = 'Name is required.'
        if not cost:
            error = 'Cost is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO item (name, description, cost, section)'
                ' VALUES (?,?,?,?)',
                (name, desc, cost, section)
            )
            db.commit()
            return redirect( url_for('menu.index') )
    return render_template( 'add_item.html', sections=sections )

def get_all_sections():
    sections = get_db().execute(
        'SELECT name FROM section'
    ).fetchall()
    if sections is None:
        abort( 404, "No sections found" )
    return sections

def get_item(id):
    item = get_db().execute(
        'SELECT id, i.name, description, cost, section, s.name'
        ' FROM item i JOIN section s ON i.section = s.name'
        ' WHERE id=?',
        (id,)
    ).fetchone()

    if item is None:
        abort( 404, "Item id {0} doesn't exist.".format(id) )

    return item

from flask import (
    Blueprint, request, redirect, url_for, flash, render_template
)
from werkzeug.exceptions import abort
from app.db import get_db
import app.util as util

bp = Blueprint('menu', __name__)

@bp.route('/')
def index():
    sections = util.get_all_sections()
    section_names_desc = [ (s['name'], s['description']) for s in sections ]
    items_by_section = {}
    for s in section_names_desc:
        items_by_section[s] = util.get_items_by_section(s[0])

    return render_template('index.html', items_by_section=items_by_section)

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
    sections = util.get_all_sections()
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

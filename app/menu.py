from flask import (
    Blueprint, request, g, redirect, url_for, flash, render_template
)
from werkzeug.exceptions import abort
from app.db import get_db
from app.auth import login_required
import app.util as util

bp = Blueprint('menu', __name__, url_prefix='/menu')

@bp.route('/index', methods=('GET', 'POST'))
def index():
    menu_data = util.get_menus_data()
    if request.method == 'POST':
        filters = request.form.getlist('filters') # list of filters
        meny_data = filter_menu_data(menu_data, filters)
    return render_template('menu/menu.html', menu_data=menu_data)

@bp.route('/<menu>/add_section', methods=('GET', 'POST'))
@login_required(types=['Manager'])
def add_section(menu):
    ''' adds a new menu section '''
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']

        db = get_db()
        db.execute(
            'INSERT INTO section (name, description, menu)'
            ' VALUES (?,?,?)',
            (name, desc, menu)
        )
        db.commit()
        return redirect( url_for('.index') )
    return render_template( 'menu/add_section.html', menu=menu )

@bp.route('/<menu>/edit_section', methods=('GET', 'POST'))
@login_required(types=['Manager'])
def edit_section(menu):
    ''' edits/deletes an existing menu section '''
    sections = { s['name'] : s['description'] for s in \
                 util.get_sections_by_menu(menu)
               }
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        section = request.form['section']

        if request.form['action'] == 'Delete':
            util.delete_section(section, menu)
        else:
            util.edit_section(name, desc, section, menu)

        return redirect( url_for('.index') )
    return render_template( 'menu/edit_section.html', sections=sections, menu=menu )

@bp.route('/<menu>/add_item', methods=('GET', 'POST'))
@login_required(types=['Manager'])
def add_item(menu):
    ''' adds a new menu item to the database '''
    sections = [ s['name'] for s in util.get_sections_by_menu(menu) ]
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        cost = request.form['cost']
        section = request.form['section']
        diet = request.form['diet']
        spicy = request.form['spicy']

        db = get_db()
        db.execute(
            'INSERT INTO item'
            ' (name, description, cost, section, menu, diet, spicy)'
            ' VALUES (?,?,?,?,?,?,?)',
            (name, desc, cost, section, menu, diet, spicy)
        )
        db.commit()
        return redirect( url_for('.index') )
    return render_template( 'menu/add_item.html', sections=sections, menu=menu )

@bp.route('/<menu>/edit_item', methods=('GET', 'POST'))
@login_required(types=['Manager'])
def edit_item(menu):
    ''' edits/deletes the given item from the menu '''
    items = util.get_items_by_menu(menu)
    sections = [ s['name'] for s in util.get_sections_by_menu(menu) ]
    items_by_id = {}
    for i in items:
        items_by_id[ str(i['id']) ] = {
            'name': i['name'], 'description': i['description'],
            'cost': i['cost'], 'section': i['section'],
            'diet': i['diet'], 'spicy': i['spicy']
        }

    if request.method == 'POST':
        id = request.form['item']
        name = request.form['name']
        desc = request.form['description']
        cost = request.form['cost']
        section = request.form['section']
        diet = request.form['diet']
        spicy = request.form['spicy']

        if request.form['action'] == 'Delete':
            util.delete_item(id)
        else:
            util.edit_item(id, name, desc, cost, section, diet, spicy)

        return redirect( url_for('.index') )
    return render_template( 'menu/edit_item.html', items=items_by_id,
                            sections=sections, menu=menu )

def filter_menu_data(menu_data, filters):
    ''' filter the items to be shown to the user '''
    if not filters:
        return menu_data
    for menu, section in menu_data.items():
        for sec, items in section.items():
            filtered_items = filter(lambda x : any( fltr in filters for fltr in [x['diet'], x['spicy']] ), items)
            menu_data[menu][sec] = list(filtered_items)
    return menu_data

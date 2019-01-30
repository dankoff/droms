'''
Utility functions
'''
from app.db import get_db
from werkzeug.exceptions import abort

def get_menus_data():
    ''' returns a dict as described below
    where each item is a dict with column name as the key

    { (menu1_name, menu1_desc) : {
                                (sec1_name, sec1_desc) : [ item1, ..., itemN ],
                                ...
                                (secN_name, secN_desc) : [ item1, ..., itemN ]
                                 }
      (menu2_name, menu2_desc) : { ... }
    }
    '''
    menus = [ (m['name'], m['description']) for m in get_menus() ]
    ret = {}
    for m in menus:
        ret[m] = {}
        sections = [ (s['name'], s['description']) \
                    for s in get_sections_by_menu(m[0]) ]
        for s in sections:
            items = get_items_by_section_and_menu(s[0], m[0])
            ret[m][s] = items
    return ret

def get_all_sections():
    ''' returns all section records from all menus '''
    sections = get_db().execute(
        'SELECT name, description, menu FROM section ORDER BY menu ASC'
    ).fetchall()
    if sections is None:
        abort( 404, "No sections found" )
    return sections

def get_sections_by_menu(menu):
    ''' returns all section records given a menu '''
    sections = get_db().execute(
        'SELECT name, description FROM section WHERE menu=?',
        (menu,)
    ).fetchall()
    if sections is None:
        abort( 404, "No sections found for menu {0}".format(menu) )
    return sections

def get_section_by_name_and_menu(name, menu):
    ''' returns a section record given its name and menu '''
    section = get_db().execute(
        'SELECT name, description, menu FROM section'
        ' WHERE name=? and menu=?',
        (name, menu)
    ).fetchone()
    if section is None:
        abort( 404, "Section {0} not found in {1}".format(name, menu) )
    return section

def get_items_by_section_and_menu(section, menu):
    ''' returns all item records given a section and menu '''
    items = get_db().execute(
        'SELECT id, name, description, cost, diet, spicy'
        ' FROM item'
        ' WHERE section=? AND menu=?'
        ' ORDER BY cost ASC',
        (section, menu)
    ).fetchall()
    if items is None:
        abort( 404, "No items found in section {0}, {1}".format(section, menu) )
    return items

def get_items_by_menu(menu):
    ''' returns all item records given a menu '''
    items = get_db().execute(
        'SELECT id, name, description, cost, section, diet, spicy'
        ' FROM item WHERE menu=?', (menu,)
    ).fetchall()
    if items is None:
        abort( 404, "No items found in {0}".format(menu) )
    return items

def get_all_items():
    ''' returns all item records '''
    items = get_db().execute(
        'SELECT id, name, description, cost, diet, spicy FROM item'
    ).fetchall()
    if items is None:
        about( 404, "No items found" )
    return items

def get_items_by_diet(diet):
    ''' returns all item records given a diet '''
    items = get_db().execute(
        'SELECT * FROM item WHERE diet=?',
        (diet,)
    ).fetchall()
    if items is None:
        abort(404, "No {0} items found".format(diet))
    return items

def get_item_by_id(id):
    ''' returns the item matching the id given '''
    item = get_db().execute(
        'SELECT name, description, cost, diet, spicy'
        ' FROM item WHERE id=?', (id,)
    ).fetchone()
    if item is None:
        abort(404, "Item {0} not found.".format(id))
    return item

def get_work_places():
    ''' returns a list of all work places '''
    work_places = get_db().execute(
        'SELECT name FROM workPlace'
    ).fetchall()
    if work_places is None:
        abort( 404, "No work places found." )
    return [ p['name'] for p in work_places ]

def get_menus():
    ''' returns all menu records '''
    menus = get_db().execute(
        'SELECT name, description FROM menu'
    ).fetchall()
    if menus is None:
        abort( 404, "No menus found." )
    return menus

def edit_item(id, name, desc, cost, section, diet, spicy):
    ''' updates a given item in the database '''
    db = get_db()
    db.execute(
        'UPDATE item SET name=?, description=?,'
        ' cost=?, section=?, diet=?, spicy=?'
        ' WHERE id=?',
        (name, desc, cost, section, diet, spicy, id)
    )
    db.commit()

def delete_item(id):
    ''' deletes an item in the database given its id '''
    db = get_db()
    db.execute(
        'DELETE FROM item WHERE id=?', (id,)
    )
    db.commit()

def edit_section(name, desc, section, menu):
    ''' updates a given section in the database '''
    db = get_db()
    # update section table
    db.execute(
        'UPDATE section SET name=?, description=?'
        ' WHERE name=? AND menu=?',
        (name, desc, section, menu)
    )
    db.commit()
    # update item table
    db.execute(
        'UPDATE item SET section=?'
        ' WHERE section=?',
        (name, section)
    )
    db.commit()

def delete_section(section, menu):
    ''' deletes the given section in the given menu along with its items '''
    db = get_db()
    # delete the section
    db.execute(
        'DELETE FROM section WHERE name=? AND menu=?',
        (section, menu)
    )
    db.commit()
    # delete all its items
    db.execute(
        'DELETE FROM item WHERE section=? AND menu=?',
        (section, menu)
    )
    db.commit()

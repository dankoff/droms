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
    sections = get_db().execute(
        'SELECT name, description, menu FROM section ORDER BY menu ASC'
    ).fetchall()
    if sections is None:
        abort( 404, "No sections found" )
    return sections

def get_sections_by_menu(menu):
    sections = get_db().execute(
        'SELECT name, description FROM section WHERE menu=?',
        (menu,)
    ).fetchall()
    if sections is None:
        abort( 404, "No sections found for menu {0}".format(menu) )
    return sections

def get_section_by_name_and_menu(name, menu):
    section = get_db().execute(
        'SELECT name, description, menu FROM section'
        ' WHERE name=? and menu=?',
        (name, menu)
    ).fetchone()
    if section is None:
        abort( 404, "Section {0} in menu {1} not found".format(name, menu))
    return section

def get_items_by_section_and_menu(section, menu):
    items = get_db().execute(
        'SELECT name, description, cost'
        ' FROM item'
        ' WHERE section=? AND menu=?'
        ' ORDER BY cost ASC',
        (section, menu)
    ).fetchall()
    return items

def get_menus():
    menus = get_db().execute(
        'SELECT name, description FROM menu'
    ).fetchall()
    return menus

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

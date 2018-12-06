'''
Utility functions
'''
from app.db import get_db
from werkzeug.exceptions import abort

def get_all_sections():
    sections = get_db().execute(
        'SELECT * FROM section'
    ).fetchall()
    if sections is None:
        abort( 404, "No sections found" )
    return sections

def get_items_by_section(section_name):
    items = get_db().execute(
        'SELECT name, description, cost FROM item '
        ' WHERE section=?'
        ' ORDER BY name ASC',
        (section_name,)
    ).fetchall()

    return items

def get_item_by_id(id):
    item = get_db().execute(
        'SELECT id, i.name, description, cost, section, s.name'
        ' FROM item i JOIN section s ON i.section = s.name'
        ' WHERE id=?',
        (id,)
    ).fetchone()

    if item is None:
        abort( 404, "Item id {0} doesn't exist.".format(id) )

    return item

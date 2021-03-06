'''
Utility functions
'''
from app.db import get_db
from datetime import date
from flask import flash

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

def get_sections_by_menu(menu):
    ''' returns all section records given a menu '''
    sections = get_db().execute(
        'SELECT name, description FROM section WHERE menu=?',
        (menu,)
    ).fetchall()
    return sections

def get_items_by_section_and_menu(section, menu):
    ''' returns all item records given a section and menu '''
    items = get_db().execute(
        'SELECT id, name, description, cost, diet, spicy'
        ' FROM item'
        ' WHERE section=? AND menu=?'
        ' ORDER BY cost ASC',
        (section, menu)
    ).fetchall()
    return items

def get_items_by_menu(menu):
    ''' returns all item records given a menu '''
    items = get_db().execute(
        'SELECT id, name, description, cost, section, diet, spicy'
        ' FROM item WHERE menu=?', (menu,)
    ).fetchall()
    return items

def get_item_by_id(id):
    ''' returns the item matching the id given '''
    item = get_db().execute(
        'SELECT name, description, cost, diet, spicy'
        ' FROM item WHERE id=?', (id,)
    ).fetchone()
    if item is None:
        flash( "Item {0} not found.".format(id) )
    return item

def get_work_places():
    ''' returns a list of all work places '''
    work_places = get_db().execute(
        'SELECT name FROM workPlace'
    ).fetchall()
    if len(work_places) == 0:
        flash( "No work places found." )
    return [ p['name'] for p in work_places ]

def get_menus():
    ''' returns all menu records '''
    menus = get_db().execute(
        'SELECT name, description FROM menu'
    ).fetchall()
    if len(menus) == 0:
        flash( "No menus found." )
    return menus

def get_restaurants():
    ''' returns all restaurant records '''
    restaurants = get_db().execute(
        'SELECT * FROM restaurant'
    ).fetchall()
    if len(restaurants) == 0:
        flash( "No restaurants found." )
    return restaurants

def get_orders_by_date(date=None):
    ''' retrieves all orders for the given date in the format yyyy-mm-dd '''
    orders = []
    if date:
        db = get_db()
        orders = db.execute(
            'SELECT id, tableNo, created, completed'
            ' FROM custOrder'
            ' WHERE created LIKE ?', (date+'%',)
        ).fetchall()
    return orders

def get_order_by_id(id):
    ''' retrieves order details for the given order id '''
    db = get_db()
    order = db.execute(
        'SELECT orderId, itemId, tableNo, created, name, description, diet, spicy, quantity'
        ' FROM orderDetail o'
        ' JOIN item i ON o.itemId = i.id'
        ' JOIN custOrder co ON o.orderId = co.id'
        ' WHERE co.id=?', (id,)
    ).fetchall()
    return order

def get_tables(restName):
    ''' retrieves all tables for the given restaurant name '''
    db = get_db()
    tables = db.execute(
        'SELECT tableNo, noOfSeats, seatsLeft, free'
        ' FROM restTable'
        ' WHERE restName=?', (restName,)
    ).fetchall()
    if len(tables) == 0:
        flash( "No tables found for restaurant {}".format(restName) )
    return tables

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

def complete_order(orderId):
    ''' marks a pending order as complete '''
    db = get_db()
    # update custOrder table
    db.execute(
        'UPDATE custOrder SET completed=?'
        ' WHERE id=?',
        (1, orderId)
    )
    db.commit()

def pay_bill(orderIDs):
    ''' marks the given orders as paid '''
    db = get_db()
    for id in orderIDs:
        db.execute(
            'UPDATE custOrder SET paid=? WHERE id=?',
            (1, id)
        )
        db.commit()

def generate_bill(tblNo, ip):
    ''' pulls all items ordered by the customer for the day '''
    today = date.today().strftime('%Y-%m-%d')
    db = get_db()
    # get all items ordered today for the given ip address, i.e. customer
    billItems = db.execute(
        'SELECT co.id, name, description, diet, spicy, quantity, cost, paid'
        ' FROM orderDetail o'
        ' JOIN item i ON o.itemId = i.id'
        ' JOIN custOrder co ON o.orderId = co.id'
        ' WHERE co.custIP=? AND co.tableNo=? AND created LIKE ?'
        ' AND paid=?', (ip, tblNo, today+'%', 0)
    ).fetchall()
    return billItems

def save_message(src, msg):
    ''' stores the given message to the database '''
    db = get_db()
    db.execute(
        'INSERT INTO communication (source, message)'
        ' VALUES (?,?)', (src, msg)
    )
    db.commit()

def get_last3_messages(src):
    ''' gets the last 3 saved messages by src from the communication table '''
    today = date.today().strftime('%Y-%m-%d')
    db = get_db()
    msgs = db.execute(
        'SELECT timeSent, message FROM communication'
        ' WHERE source=? AND timeSent LIKE ?'
        ' ORDER BY timeSent DESC LIMIT 3',
        (src, today + '%')
    ).fetchall()
    return msgs

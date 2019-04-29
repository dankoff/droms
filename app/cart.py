from flask import (
    Blueprint, request, g, redirect, url_for, flash, render_template, session
)
from werkzeug.exceptions import abort
from app.db import get_db
from app.util import get_item_by_id, generate_bill, pay_bill, save_message

bp = Blueprint('cart', __name__)

@bp.route('/view_cart')
def view_cart():
    if not g.user:
        items_by_id = session.get('cart', None)
        return render_template( 'cart/cart.html', items=items_by_id )
    return redirect( url_for('menu.index') )

@bp.route('/add_to_cart/item_<int:item_id>')
def add_to_cart(item_id):
    ''' adds the item with the given id to the order '''
    i = get_item_by_id(item_id)
    if i:
        item_id = str(item_id)
        item_details = { 'name' : i['name'], 'description' : i['description'], \
                         'cost' : i['cost'], 'diet' : i['diet'], 'id' : item_id, \
                         'spicy' : i['spicy'], 'total_cost' : i['cost'], 'qty' : 1 }
        if 'cart' not in session:
            session['cart'] = [ item_details ]
        else:
            item_idx = next((idx for idx, s in enumerate(session['cart']) if s['id'] == item_id), None)
            if item_idx is not None:
                session['cart'][item_idx]['qty'] += 1
                session['cart'][item_idx]['total_cost'] += i['cost']
            else:
                session['cart'].append(item_details)
            session.modified = True

    return redirect( url_for('menu.index') )

@bp.route('/make_order/total_<float:total>')
def make_order(total):
    ''' store customer order details to the database '''
    # ensure user has selected a table first
    if 'tableNo' not in session:
        flash("You must select a table before you can place an order.")
        return redirect( url_for('index') )
    if 'cart' in session:
        db = get_db()
        custIP = session.get('custIP', request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
        orderId = db.execute(
            'INSERT INTO custOrder'
            ' (custIP, totalCost, tableNo)'
            ' VALUES (?, ?, ?)',
            (custIP, total, session['tableNo'])
        ).lastrowid
        db.commit()
        if orderId is not None:
            for i in session['cart']:
                db.execute(
                    'INSERT INTO orderDetail'
                    ' (itemId, orderId, quantity)'
                    ' VALUES (?, ?, ?)',
                    (int(i['id']), orderId, i['qty'])
                )
                db.commit()
            session.pop('cart', None)
            flash("Order submitted!")
    return redirect( url_for('cart.view_cart') )

@bp.route('/update_cart/item_<int:id>/action_<action>')
def update_cart(id, action):
    ''' updates the order for the item with the given id and action to perform '''
    if 'cart' in session:
        item_id = str(id)
        item_idx = next((idx for idx, i in enumerate(session['cart']) if i['id'] == item_id), None)
        if item_idx is not None:
            if action in ['inc', 'dec']:
                updateQuantity(item_idx, action)
            elif action == 'remove':
                del session['cart'][item_idx]
                session.modified = True
    return redirect( url_for('cart.view_cart') )

def updateQuantity(item_idx, action):
    ''' updates the quantity of the item at the given item_idx '''
    cost = session['cart'][item_idx]['cost']
    qty = session['cart'][item_idx]['qty']
    if action == 'inc':
        if qty < 30:
            session['cart'][item_idx]['qty'] += 1
            session['cart'][item_idx]['total_cost'] += cost
            session.modified = True
    else:
        if qty > 1:
            session['cart'][item_idx]['qty'] -= 1
            session['cart'][item_idx]['total_cost'] -= cost
            session.modified = True

@bp.route('/view_bill', methods=('GET', 'POST'))
def view_bill():
    ''' retrieves and groups the currently unpaid items to generate a bill '''
    itemsByName = {}
    tblNo = session.get('tableNo', None)
    custIP = session.get('custIP', request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    billItems = generate_bill(tblNo, custIP)
    if request.method == 'POST':
        billTotal = request.form['bill_total']
        request_bill(billItems, billTotal)
    else:
        if billItems is not None:
            itemsByName = groupBillItems(billItems)
    return render_template( 'cart/bill.html', items=itemsByName )

def groupBillItems(billItems):
    ''' group the bill items in a dictionary ensuring
        identical items are not shown separately
    '''
    itemsByName = {}
    for i in billItems:
        if i['name'] not in itemsByName:
            itemsByName[i['name']] = { 'desc' : i['description'], 'cost' : i['cost'] * i['quantity'], \
            'qty' : i['quantity'], 'diet' : i['diet'], 'spicy' : i['spicy'] }
        else:
            qty = itemsByName[i['name']]['qty'] + i['quantity']
            itemsByName[i['name']]['qty'] = qty
            itemsByName[i['name']]['cost'] = i['cost'] * qty
    return itemsByName

def request_bill(billItems, billTotal):
    ''' marks the orders associated with the given items as paid '''
    orderIDs = set([ i['id'] for i in billItems ])
    if orderIDs:
        # there are unpaid items
        pay_bill(orderIDs)
        msg = 'A customer from table {} has requested the bill totalling £{:.2f}'.format( \
        session.get('tableNo', None), float(billTotal) )
        save_message('Kitchen', msg)
        flash('Thank you, a member of the waiting staff will be with you shortly.')

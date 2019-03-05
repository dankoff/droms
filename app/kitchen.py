from flask import (
    Blueprint, request, redirect, url_for, render_template, g, jsonify
)
from werkzeug.exceptions import abort
from datetime import date
from app.db import get_db
from app.auth import login_required
from app.util import (
    get_all_orders, get_orders_by_date, get_order_by_id, complete_order,
    save_message, get_last3_messages
)

bp = Blueprint('kitchen', __name__, url_prefix='/kitchen',
                static_folder='static')

@bp.route('/home')
@login_required(types=[])
def home():
    return render_template( 'kitchen/kitchen.html' )

@bp.route('/order/complete')
@login_required(types=['Cook'])
def completeOrder():
    id = request.args.get('orderId', None)
    msg = request.args.get('message', None)
    src = request.args.get('source', 'Kitchen', type=str)
    aDate = request.args.get('selDate', str(date.today()), type=str)
    
    if id:
        complete_order(id)
    if msg:
        save_message(src, msg)
    orders = showOrders(aDate)
    return jsonify(orders)

@bp.route('/order')
@login_required(types=[])
def showOrder():
    id = request.args.get('orderId')
    orderDetails = itemsByOrder(id)
    return jsonify(orderDetails)

@bp.route('/home/orders')
@login_required(types=[])
def ordersByDate():
    aDate = request.args.get('selDate', str(date.today()), type=str)
    orders = showOrders(aDate)
    return jsonify(orders)

@bp.route('/home/send_message')
@login_required(types=['Cook', 'Waiter'])
def send_message():
    msg = request.args.get('message', None)
    src = request.args.get('source', None)
    res = list()
    if msg and src:
        save_message(src, msg)
        res = messageDataDict(src)
    return jsonify(res)

@bp.route('/home/messages')
@login_required(types=['Cook', 'Waiter'])
def loadMessages():
    src = request.args.get('source', None)
    res = list()
    if src:
        res = messageDataDict(src)
    return jsonify(res)

def messageDataDict(src):
    res = list()
    data = get_last3_messages(src)
    if data is not None:
        for row in data:
            msgData = { 'msg' : row['message'], 'datetime' : row['timeSent'].strftime("%H:%M:%S") }
            res.append(msgData)
    return res

def showOrders(aDate=None):
    ''' displays all orders for the given date '''
    if not aDate:
        # returns today's date in the format yyyy-mm-dd
        aDate = str(date.today())
    orders = get_orders_by_date(aDate)
    data = []
    for o in orders:
        data.append(dict(id=o['id'], tableNo=o['tableNo'],
                             created=o['created'].strftime('%-d %b %Y at %H:%M:%S'),
                             completed=o['completed']))
    return data

def itemsByOrder(id):
    orderDetails = get_order_by_id(id)
    itemsByOrder = []
    for i in orderDetails:
        item_details = { 'orderId' : i['orderId'], 'tableNo' : i['tableNo'],
                         'created' : i['created'].strftime('%-d %b %Y at %H:%M:%S'),
                         'name' : i['name'], 'diet' : i['diet'], 'desc' : i['description'],
                         'spicy' : i['spicy'], 'quantity' : i['quantity'] }
        itemsByOrder.append(item_details)
    return itemsByOrder

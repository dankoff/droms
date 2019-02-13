from flask import (
    Blueprint, request, redirect, url_for, render_template, g, jsonify
)
from werkzeug.exceptions import abort
from datetime import date
from app.db import get_db
from app.auth import login_required
from app.util import get_all_orders, get_orders_by_date, get_order_by_id

bp = Blueprint('kitchen', __name__, url_prefix='/kitchen',
                static_folder='static')

@bp.route('/home')
@login_required(types=['Manager', 'Cook'])
def home():
    return render_template( 'kitchen/kitchen.html' )

@bp.route('/order')
@login_required(types=['Manager', 'Cook'])
def showOrder():
    id = request.args.get('orderId')
    orderDetails = itemsByOrder(id)
    return jsonify(orderDetails)

@bp.route('/home/orders')
@login_required(types=['Manager', 'Cook'])
def ordersByDate():
    aDate = request.args.get('selDate', str(date.today()), type=str)
    orders = showOrders(aDate)
    return jsonify(orders)

def showOrders(aDate=None):
    ''' displays all orders for the given date '''
    if not aDate:
        # returns today's date in the format yyyy-mm-dd
        aDate = str(date.today())
    orders = get_orders_by_date(aDate)
    data = []
    for o in orders:
        data.append(dict(id=o['id'], tableNo=o['tableNo'],
                             created=o['created'].strftime('%-d %b %Y at %H:%M:%S')))
    return data

def itemsByOrder(id):
    orderDetails = get_order_by_id(id)
    itemsByOrder = []
    for i in orderDetails:
        item_details = { 'orderId' : i['orderId'], 'tableNo' : i['tableNo'],
                         'created' : i['created'].strftime('%-d %b %Y at %H:%M:%S'),
                         'name' : i['name'], 'diet' : i['diet'],
                         'spicy' : i['spicy'], 'quantity' : i['quantity'] }
        itemsByOrder.append(item_details)
    return itemsByOrder

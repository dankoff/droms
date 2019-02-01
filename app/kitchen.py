from flask import (
    Blueprint, request, redirect, url_for, render_template, g
)
from werkzeug.exceptions import abort
from app.db import get_db
from app.auth import login_required
from app.util import get_all_orders

bp = Blueprint('kitchen', __name__, url_prefix='/kitchen',
                static_folder='static')

@bp.route('/home')
@login_required
def home():
    if g.user['type'] == 'Cook':
        orderDetail = itemsByOrder()
        return render_template( 'kitchen/kitchen.html', orderDetail=orderDetail )
    return redirect( url_for('index') )

def itemsByOrder():
    orderDetail = get_all_orders()
    itemsByOrder = {}
    for od in orderDetail:
        key = (od['orderId'], od['tableNo'])
        item_details = { 'name' : od['name'], 'diet' : od['diet'],
                         'spicy' : od['spicy'], 'qty' : od['quantity'] }
        if key not in itemsByOrder:
            itemsByOrder[key] = [item_details]
        else:
            itemsByOrder[key].append(item_details)
    return itemsByOrder

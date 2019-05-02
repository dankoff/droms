from flask import (
    Blueprint, redirect, request, render_template, session, url_for, flash
)

from app.db import get_db
from app.util import get_tables, get_restaurants

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    if 'custIP' not in session:
        visitorIP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        session['custIP'] = visitorIP
    restaurants = get_restaurants()
    tables = get_tables(restaurants[0]['name'])
    return render_template('index.html', tables=tables)

@bp.route('/freeseat')
def free_seat():
    tblNo = session.get('tableNo', None)
    if tblNo:
        freeSeat(tblNo)
    return redirect( url_for('index') )

@bp.route('/table_selection/table_<int:id>')
def table_selection(id):
    ''' '''
    def take_seat(tableNo, seatsLeft):
        if 'tableNo' not in session:
            session['tableNo'] = tableNo
            db.execute(
                'UPDATE restTable SET seatsLeft=? WHERE tableNo=?', (seatsLeft-1, tableNo)
            )
            db.commit()

    db = get_db()
    td = db.execute(
        'SELECT seatsLeft, free FROM restTable WHERE tableNo=?', (id,)
    ).fetchone()
    if td['free']:
        take_seat(id, td['seatsLeft'])
        if get_seats_left(db, id) == 0:
            db.execute(
                'UPDATE restTable SET free=? WHERE tableNo=?', (0, id)
            )
            db.commit()
    return redirect( url_for('menu.index') )

def freeSeat(tableNo):
    db = get_db()
    seatsLeft = get_seats_left(db, tableNo)
    db.execute(
        'UPDATE restTable SET seatsLeft=?, free=?'
        ' WHERE tableNo=?', (seatsLeft+1, 1, tableNo)
    )
    db.commit()
    session.pop('tableNo', None)

def get_seats_left(db, tableNo):
    td = db.execute(
        'SELECT seatsLeft FROM restTable WHERE tableNo=?', (tableNo,)
    ).fetchone()
    return td['seatsLeft']

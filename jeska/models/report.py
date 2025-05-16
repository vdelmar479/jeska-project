from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('report', __name__, url_prefix='/reports')

# Index - List all reports
@bp.route('/')
@login_required
def index():
    db = get_db()
    reports = db.execute(
        'SELECT r.id, r.title, r.body, r.author_username, r.device_name, r.status, r.created_at'
        ' FROM reports r'
        ' ORDER BY r.created_at DESC'
    ).fetchall()
    
    # Get user role
    user = db.execute(
        'SELECT role FROM users WHERE username = ?',
        (g.user['username'],)
    ).fetchone()
    
    is_admin = user['role'] == 'admin' if user and user['role'] else False
    
    return render_template('report/index.html', reports=reports, is_admin=is_admin)

# Create a report
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        device_name = request.form['device_name']
        status = request.form['status']
        error = None

        if not title:
            error = 'Title is required.'
        if not device_name:
            error = 'Device name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO reports (title, body, author_username, device_name, status, created_at)'
                    ' VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)',
                    (title, body, g.user['username'], device_name, status)
                )
                db.commit()
                return redirect(url_for('report.index'))
            except db.IntegrityError:
                error = f"Device {device_name} does not exist."
                flash(error)

    # Get list of devices for the dropdown
    db = get_db()
    devices = db.execute('SELECT name FROM devices').fetchall()
    return render_template('report/create.html', devices=devices)

# Get a report
def get_report(id, check_author=True):
    report = get_db().execute(
        'SELECT r.id, r.title, r.body, r.author_username, r.device_name, r.status, r.created_at'
        ' FROM reports r'
        ' WHERE r.id = ?',
        (id,)
    ).fetchone()

    if report is None:
        abort(404, f"Report id {id} doesn't exist.")

    if check_author and report['author_username'] != g.user['username']:
        # Check if user is admin
        db = get_db()
        user = db.execute(
            'SELECT role FROM users WHERE username = ?',
            (g.user['username'],)
        ).fetchone()
        
        if not user or user['role'] != 'admin':
            abort(403)

    return report

# View a report (read-only)
@bp.route('/<int:id>/view')
@login_required
def view(id):
    # Get the report without checking author (any logged in user can view)
    report = get_report(id, check_author=False)
    return render_template('report/view.html', report=report)

# Update a report
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    report = get_report(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        device_name = request.form['device_name']
        status = request.form['status']
        error = None

        if not title:
            error = 'Title is required.'
        if not device_name:
            error = 'Device name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            try:
                db.execute(
                    'UPDATE reports SET title = ?, body = ?, device_name = ?, status = ?'
                    ' WHERE id = ?',
                    (title, body, device_name, status, id)
                )
                db.commit()
                return redirect(url_for('report.index'))
            except db.IntegrityError:
                error = f"Device {device_name} does not exist."
                flash(error)

    # Get list of devices for the dropdown
    db = get_db()
    devices = db.execute('SELECT name FROM devices').fetchall()
    return render_template('report/update.html', report=report, devices=devices)

# Delete a report
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_report(id)
    db = get_db()
    db.execute('DELETE FROM reports WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('report.index')) 
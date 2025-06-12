from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import mysql.connector

from .auth import login_required
from .db import get_db
from .. import config

bp = Blueprint('report', __name__, url_prefix='/reports')

# Index - List all reports
@bp.route('/')
@login_required
def index():
    db, cursor = get_db()
    cursor.execute(
        'SELECT r.id, r.title, r.body, r.author_username, r.device_name, r.status, r.created_at'
        ' FROM reports r'
        ' ORDER BY r.created_at DESC'
    )
    reports = cursor.fetchall()
    
    # Get user role
    cursor.execute(
        'SELECT role FROM users WHERE username = %s',
        (g.user['username'],)
    )
    user = cursor.fetchone()
    
    is_admin = user['role'] == 'admin' if user and user['role'] else False
    
    # Get list of devices for the dropdown
    cursor.execute('SELECT name FROM devices')
    devices = cursor.fetchall()
    
    return render_template('report/index.html', reports=reports, is_admin=is_admin, devices=devices, config=config)

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
            try:
                db, cursor = get_db()
                cursor.execute(
                    'INSERT INTO reports (title, body, author_username, device_name, status, created_at)'
                    ' VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)',
                    (title, body, g.user['username'], device_name, status)
                )
                db.commit()
                return redirect(url_for('report.index'))
            except mysql.connector.Error as e:
                if e.errno == 1452:  # Foreign key constraint error
                    error = f"Device {device_name} does not exist."
                else:
                    error = "Database error occurred."
                flash(error)

    return redirect(url_for('report.index'))

# Get a report
def get_report(id, check_author=True):
    db, cursor = get_db()
    cursor.execute(
        'SELECT r.id, r.title, r.body, r.author_username, r.device_name, r.status, r.created_at'
        ' FROM reports r'
        ' WHERE r.id = %s',
        (id,)
    )
    report = cursor.fetchone()

    if report is None:
        abort(404, f"Report id {id} doesn't exist.")

    # Only check author permissions if explicitly requested (for updates/deletes)
    if check_author:
        if report['author_username'] != g.user['username']:
            # Check if user is admin
            cursor.execute(
                'SELECT role FROM users WHERE username = %s',
                (g.user['username'],)
            )
            user = cursor.fetchone()
            
            if not user or user['role'] != 'admin':
                abort(403)

    return report

# Update a report
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    report = get_report(id, check_author=True)  # Explicitly check author for updates

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
            try:
                db, cursor = get_db()
                cursor.execute(
                    'UPDATE reports SET title = %s, body = %s, device_name = %s, status = %s'
                    ' WHERE id = %s',
                    (title, body, device_name, status, id)
                )
                db.commit()
                return redirect(url_for('report.index'))
            except mysql.connector.Error as e:
                if e.errno == 1452:  # Foreign key constraint error
                    error = f"Device {device_name} does not exist."
                else:
                    error = "Database error occurred."
                flash(error)

    return redirect(url_for('report.index'))

# Delete a report
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    # Check if user is admin
    db, cursor = get_db()
    cursor.execute(
        'SELECT role FROM users WHERE username = %s',
        (g.user['username'],)
    )
    user = cursor.fetchone()
    
    if not user or user['role'] != 'admin':
        abort(403)

    get_report(id, check_author=False)  # We don't need to check author since we already verified admin
    try:
        cursor.execute('DELETE FROM reports WHERE id = %s', (id,))
        db.commit()
        return redirect(url_for('report.index'))
    except mysql.connector.Error:
        flash('Error deleting report.')
        return redirect(url_for('report.index'))

@bp.route('/<int:id>/view', methods=['GET'])
@login_required
def view(id):
    report = get_report(id, check_author=False)  # Don't check author for viewing
    return render_template('report/view.html', report=report) 
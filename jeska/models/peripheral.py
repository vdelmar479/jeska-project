from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import mysql.connector

from .auth import login_required, admin_required
from .db import get_db
from .. import config

bp = Blueprint('peripheral', __name__, url_prefix='/peripherals')

# Index - List all peripherals
@bp.route('/')
@login_required
def index():
    db, cursor = get_db()
    cursor.execute(
        'SELECT p.id, p.name, p.type, p.description, p.in_use, p.total'
        ' FROM peripherals p'
        ' ORDER BY p.name ASC'
    )
    peripherals = cursor.fetchall()
    return render_template('peripheral/index.html', peripherals=peripherals, config=config)

# Create a peripheral
@bp.route('/create', methods=('GET', 'POST'))
@login_required
@admin_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        total = request.form.get('total', 0, type=int)
        error = None

        if not name:
            error = 'Peripheral name is required.'
        if not type:
            error = 'Peripheral type is required.'
        if total < 0:
            error = 'Total quantity must be non-negative.'

        if error is not None:
            flash(error, 'danger')
        else:
            try:
                db, cursor = get_db()
                cursor.execute(
                    'INSERT INTO peripherals (name, type, description, total, in_use)'
                    ' VALUES (%s, %s, %s, %s, 0)',
                    (name, type, description, total)
                )
                db.commit()
                flash('Peripheral created successfully.', 'success')
                return redirect(url_for('peripheral.index'))
            except mysql.connector.Error as e:
                if e.errno == 1062:  # Duplicate entry error
                    flash('Peripheral name already exists.', 'danger')
                else:
                    flash('Database error occurred.', 'danger')
                return redirect(url_for('peripheral.create'))

    return render_template('peripheral/create.html')

# Get a peripheral
def get_peripheral(id):
    db, cursor = get_db()
    cursor.execute(
        'SELECT p.id, p.name, p.type, p.description, p.in_use, p.total'
        ' FROM peripherals p'
        ' WHERE p.id = %s',
        (id,)
    )
    peripheral = cursor.fetchone()

    if peripheral is None:
        abort(404, f"Peripheral id {id} doesn't exist.")

    return peripheral

# Update a peripheral
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
@admin_required
def update(id):
    peripheral = get_peripheral(id)

    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        total = request.form.get('total', 0, type=int)
        error = None

        if not name:
            error = 'Peripheral name is required.'
        if not type:
            error = 'Peripheral type is required.'
        if total < peripheral['in_use']:
            error = 'Total quantity cannot be less than peripherals in use.'

        if error is not None:
            flash(error, 'danger')
        else:
            try:
                db, cursor = get_db()
                cursor.execute(
                    'UPDATE peripherals SET name = %s, type = %s, description = %s, total = %s'
                    ' WHERE id = %s',
                    (name, type, description, total, id)
                )
                db.commit()
                flash('Peripheral updated successfully.', 'success')
                return redirect(url_for('peripheral.index'))
            except mysql.connector.Error as e:
                if e.errno == 1062:  # Duplicate entry error
                    flash('Peripheral name already exists.', 'danger')
                else:
                    flash('Database error occurred.', 'danger')
                return redirect(url_for('peripheral.update', id=id))

    return render_template('peripheral/update.html', peripheral=peripheral)

# Delete a peripheral
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
@admin_required
def delete(id):
    peripheral = get_peripheral(id)
    if peripheral['in_use'] > 0:
        flash('Cannot delete peripheral that is currently in use.', 'danger')
        return redirect(url_for('peripheral.index'))
        
    try:
        db, cursor = get_db()
        cursor.execute('DELETE FROM peripherals WHERE id = %s', (id,))
        db.commit()
        flash('Peripheral deleted successfully.', 'success')
        return redirect(url_for('peripheral.index'))
    except mysql.connector.Error:
        flash('Error deleting peripheral.', 'danger')
        return redirect(url_for('peripheral.index'))

# API endpoints for AJAX operations
@bp.route('/api/peripheral/<int:id>', methods=['GET'])
@login_required
def get_peripheral_api(id):
    peripheral = get_peripheral(id)
    return jsonify({
        'id': peripheral['id'],
        'name': peripheral['name'],
        'type': peripheral['type'],
        'description': peripheral['description'],
        'in_use': peripheral['in_use'],
        'total': peripheral['total']
    })

@bp.route('/api/peripheral/<int:id>', methods=['PUT'])
@login_required
@admin_required
def update_peripheral_api(id):
    peripheral = get_peripheral(id)
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Peripheral name is required.'}), 400
    if not data.get('type'):
        return jsonify({'error': 'Peripheral type is required.'}), 400
    
    total = data.get('total', peripheral['total'])
    if total < peripheral['in_use']:
        return jsonify({'error': 'Total quantity cannot be less than peripherals in use.'}), 400

    try:
        db, cursor = get_db()
        cursor.execute(
            'UPDATE peripherals SET name = %s, type = %s, description = %s, total = %s'
            ' WHERE id = %s',
            (data['name'], data['type'], data.get('description', ''), total, id)
        )
        db.commit()
        
        return jsonify({
            'id': id,
            'name': data['name'],
            'type': data['type'],
            'description': data.get('description', ''),
            'in_use': peripheral['in_use'],
            'total': total
        })
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry error
            return jsonify({'error': 'Peripheral name already exists.'}), 400
        return jsonify({'error': 'Database error occurred.'}), 500

@bp.route('/api/peripheral', methods=['POST'])
@login_required
@admin_required
def create_peripheral_api():
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Peripheral name is required.'}), 400
    if not data.get('type'):
        return jsonify({'error': 'Peripheral type is required.'}), 400
    
    total = data.get('total', 0)
    if total < 0:
        return jsonify({'error': 'Total quantity must be non-negative.'}), 400

    try:
        db, cursor = get_db()
        cursor.execute(
            'INSERT INTO peripherals (name, type, description, total, in_use)'
            ' VALUES (%s, %s, %s, %s, 0)',
            (data['name'], data['type'], data.get('description', ''), total)
        )
        db.commit()
        
        return jsonify({
            'id': cursor.lastrowid,
            'name': data['name'],
            'type': data['type'],
            'description': data.get('description', ''),
            'in_use': 0,
            'total': total
        }), 201
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry error
            return jsonify({'error': 'Peripheral name already exists.'}), 400
        return jsonify({'error': 'Database error occurred.'}), 500

@bp.route('/consolidate', methods=['POST'])
@login_required
@admin_required
def consolidate_peripherals():
    try:
        db, cursor = get_db()
        
        # Get all devices and their peripherals
        cursor.execute(
            'SELECT peripherals FROM devices'
        )
        devices = cursor.fetchall()
        
        # Create a dictionary to count peripheral usage
        peripheral_counts = {}
        
        # Count peripherals across all devices
        for device in devices:
            if device['peripherals']:
                peripherals = device['peripherals'].split(',')
                for peripheral in peripherals:
                    peripheral = peripheral.strip()
                    if peripheral:
                        peripheral_counts[peripheral] = peripheral_counts.get(peripheral, 0) + 1
        
        # Update the in_use field for each peripheral
        for peripheral_name, count in peripheral_counts.items():
            cursor.execute(
                'UPDATE peripherals SET in_use = %s WHERE name = %s',
                (count, peripheral_name)
            )
        
        # Reset in_use to 0 for peripherals not found in any device
        if peripheral_counts:
            # If we have peripherals, use them in the NOT IN clause
            placeholders = ', '.join(['%s'] * len(peripheral_counts))
            cursor.execute(
                f'UPDATE peripherals SET in_use = 0 WHERE name NOT IN ({placeholders})',
                tuple(peripheral_counts.keys())
            )
        else:
            # If no peripherals found, reset all peripherals
            cursor.execute('UPDATE peripherals SET in_use = 0')
        
        db.commit()
        return jsonify({
            'message': 'Peripherals consolidated successfully',
            'peripheral_counts': peripheral_counts
        }), 200
        
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error occurred: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, send_file
)
from werkzeug.exceptions import abort
import json
from datetime import datetime
import io
import mysql.connector

from .auth import login_required, admin_required
from .db import get_db
from .. import config

bp = Blueprint('device', __name__, url_prefix='/devices')

def consolidate_inventory():
    """Helper function to consolidate components and peripherals usage counts"""
    try:
        db, cursor = get_db()
        
        # Get all devices and their components/peripherals
        cursor.execute(
            'SELECT components, peripherals FROM devices'
        )
        devices = cursor.fetchall()
        
        # Create dictionaries to count usage
        component_counts = {}
        peripheral_counts = {}
        
        # Count components and peripherals across all devices
        for device in devices:
            # Count components
            if device['components']:
                components = device['components'].split(',')
                for component in components:
                    component = component.strip()
                    if component:
                        component_counts[component] = component_counts.get(component, 0) + 1
            
            # Count peripherals
            if device['peripherals']:
                peripherals = device['peripherals'].split(',')
                for peripheral in peripherals:
                    peripheral = peripheral.strip()
                    if peripheral:
                        peripheral_counts[peripheral] = peripheral_counts.get(peripheral, 0) + 1
        
        # Update the in_use field for each component
        for component_name, count in component_counts.items():
            cursor.execute(
                'UPDATE components SET in_use = %s WHERE name = %s',
                (count, component_name)
            )
        
        # Reset in_use to 0 for components not found in any device
        if component_counts:
            placeholders = ', '.join(['%s'] * len(component_counts))
            cursor.execute(
                f'UPDATE components SET in_use = 0 WHERE name NOT IN ({placeholders})',
                tuple(component_counts.keys())
            )
        else:
            cursor.execute('UPDATE components SET in_use = 0')
        
        # Update the in_use field for each peripheral
        for peripheral_name, count in peripheral_counts.items():
            cursor.execute(
                'UPDATE peripherals SET in_use = %s WHERE name = %s',
                (count, peripheral_name)
            )
        
        # Reset in_use to 0 for peripherals not found in any device
        if peripheral_counts:
            placeholders = ', '.join(['%s'] * len(peripheral_counts))
            cursor.execute(
                f'UPDATE peripherals SET in_use = 0 WHERE name NOT IN ({placeholders})',
                tuple(peripheral_counts.keys())
            )
        else:
            cursor.execute('UPDATE peripherals SET in_use = 0')
        
        db.commit()
        return True
    except Exception as e:
        print(f"Error consolidating inventory: {str(e)}")
        return False

# Index - List all devices
@bp.route('/')
@login_required
def index():
    db, cursor = get_db()
    cursor.execute(
        'SELECT d.id, d.name, d.description, d.status, d.components, d.peripherals, d.location, d.buying_timestamp, d.mac_address'
        ' FROM devices d'
        ' ORDER BY d.buying_timestamp DESC'
    )
    devices = cursor.fetchall()
    
    return render_template('device/index.html', devices=devices, config=config)

# Create a device
@bp.route('/create', methods=('GET', 'POST'))
@login_required
@admin_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        components = request.form['components']
        peripherals = request.form['peripherals']
        location = request.form['location']
        error = None

        if not name:
            error = 'Device name is required.'

        if error is not None:
            flash(error)
        else:
            try:
                db, cursor = get_db()
                cursor.execute(
                    'INSERT INTO devices (name, description, status, components, peripherals, location, buying_timestamp)'
                    ' VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)',
                    (name, description, status, components, peripherals, location)
                )
                db.commit()
                
                # Consolidate inventory after successful creation
                if not consolidate_inventory():
                    flash('Device created but there was an error updating inventory counts.', 'warning')
                else:
                    flash('Device created successfully.', 'success')
                    
                return redirect(url_for('device.index'))
            except mysql.connector.Error as e:
                if e.errno == 1062:  # Duplicate entry error
                    flash('Device name already exists.')
                else:
                    flash('Database error occurred.')
                return redirect(url_for('device.create'))

    return redirect(url_for('device.index'))

# Get a device
def get_device(id, check_author=True):
    db, cursor = get_db()
    cursor.execute(
        'SELECT d.id, d.name, d.description, d.status, d.components, d.peripherals, d.location, d.buying_timestamp, d.mac_address'
        ' FROM devices d'
        ' WHERE d.id = %s',
        (id,)
    )
    device = cursor.fetchone()

    if device is None:
        abort(404, f"Device id {id} doesn't exist.")

    return device

# Update a device
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    device = get_device(id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        components = request.form['components']
        peripherals = request.form['peripherals']
        location = request.form['location']
        error = None

        if not name:
            error = 'Device name is required.'

        if error is not None:
            flash(error)
        else:
            try:
                db, cursor = get_db()
                cursor.execute(
                    'UPDATE devices SET name = %s, description = %s, status = %s, components = %s, peripherals = %s, location = %s'
                    ' WHERE id = %s',
                    (name, description, status, components, peripherals, location, id)
                )
                db.commit()
                
                # Consolidate inventory after successful update
                if not consolidate_inventory():
                    flash('Device updated but there was an error updating inventory counts.', 'warning')
                else:
                    flash('Device updated successfully.', 'success')
                    
                return redirect(url_for('device.index'))
            except mysql.connector.Error as e:
                if e.errno == 1062:  # Duplicate entry error
                    flash('Device name already exists.')
                else:
                    flash('Database error occurred.')
                return redirect(url_for('device.update', id=id))

    return redirect(url_for('device.index'))

# Delete a device
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_device(id)
    try:
        db, cursor = get_db()
        cursor.execute('DELETE FROM devices WHERE id = %s', (id,))
        db.commit()
        return redirect(url_for('device.index'))
    except mysql.connector.Error:
        flash('Error deleting device.')
        return redirect(url_for('device.index'))

# Import/Export page
@bp.route('/import-export', methods=['GET'])
@login_required
@admin_required
def import_export():
    return render_template('device/import_export.html')

# Export all devices as JSON
@bp.route('/export', methods=['GET'])
@login_required
@admin_required
def export_devices():
    db, cursor = get_db()
    cursor.execute(
        'SELECT d.id, d.name, d.description, d.status, d.components, d.peripherals, d.location, d.buying_timestamp, d.mac_address'
        ' FROM devices d'
        ' ORDER BY d.buying_timestamp DESC'
    )
    devices = cursor.fetchall()
    
    # Convert devices to list of dictionaries
    devices_list = []
    for device in devices:
        device_dict = {
            'id': device['id'],
            'name': device['name'],
            'description': device['description'],
            'status': device['status'],
            'components': device['components'].split(',') if device['components'] else [],
            'peripherals': device['peripherals'].split(',') if device['peripherals'] else [],
            'location': device['location'],
            'buying_timestamp': device['buying_timestamp'],
            'mac_address': device['mac_address']
        }
        devices_list.append(device_dict)
    
    # Create a file-like object in memory
    output = io.StringIO()
    json.dump(devices_list, output, indent=2, default=str)
    output.seek(0)
    
    # Return the file as a download
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='application/json',
        as_attachment=True,
        download_name=f'devices_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    )

# Import devices from JSON
@bp.route('/import', methods=['POST'])
@login_required
@admin_required
def import_devices():
    if 'file' not in request.files:
        flash('No file provided', 'danger')
        return redirect(url_for('device.index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('device.index'))
    
    if not file.filename.endswith('.json'):
        flash('File must be a JSON file', 'danger')
        return redirect(url_for('device.index'))
    
    try:
        devices = json.load(file)
        if not isinstance(devices, list):
            flash('JSON must contain an array of devices', 'danger')
            return redirect(url_for('device.index'))
        
        db, cursor = get_db()
        imported_count = 0
        errors = []
        
        for device in devices:
            try:
                # Validate required fields
                if 'name' not in device:
                    errors.append(f"Device missing required field 'name'")
                    continue
                
                # Convert lists back to comma-separated strings
                components = ','.join(device.get('components', [])) if isinstance(device.get('components'), list) else device.get('components', '')
                peripherals = ','.join(device.get('peripherals', [])) if isinstance(device.get('peripherals'), list) else device.get('peripherals', '')
                
                # Insert or update device
                cursor.execute(
                    'INSERT INTO devices (name, description, status, components, peripherals, location, buying_timestamp, mac_address)'
                    ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                    ' ON DUPLICATE KEY UPDATE'
                    ' description = VALUES(description),'
                    ' status = VALUES(status),'
                    ' components = VALUES(components),'
                    ' peripherals = VALUES(peripherals),'
                    ' location = VALUES(location),'
                    ' buying_timestamp = VALUES(buying_timestamp),'
                    ' mac_address = VALUES(mac_address)',
                    (
                        device['name'],
                        device.get('description', ''),
                        device.get('status', ''),
                        components,
                        peripherals,
                        device.get('location', ''),
                        device.get('buying_timestamp', datetime.now().isoformat()),
                        device.get('mac_address', '')
                    )
                )
                imported_count += 1
                
            except mysql.connector.Error as e:
                errors.append(f"Error importing device {device.get('name', 'unknown')}: {str(e)}")
        
        db.commit()
        
        if errors:
            flash(f'Successfully imported {imported_count} devices, but some errors occurred: {errors}', 'warning')
        else:
            flash(f'Successfully imported {imported_count} devices', 'success')
        return redirect(url_for('device.index'))
        
    except json.JSONDecodeError:
        flash('Invalid JSON file', 'danger')
        return redirect(url_for('device.index'))
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'danger')
        return redirect(url_for('device.index'))

# View device details and associated reports
@bp.route('/<int:id>/view', methods=['GET'])
@login_required
def view_device(id):
    db, cursor = get_db()
    cursor.execute(
        'SELECT d.id, d.name, d.description, d.status, d.components, d.peripherals, d.location, d.buying_timestamp'
        ' FROM devices d'
        ' WHERE d.id = %s',
        (id,)
    )
    device = cursor.fetchone()
    if device is None:
        abort(404, f"Device id {id} doesn't exist.")

    # Fetch reports associated with this device (by device name)
    cursor.execute(
        'SELECT r.id, r.title, r.body, r.status, r.author_username, r.created_at'
        ' FROM reports r'
        ' WHERE r.device_name = %s'
        ' ORDER BY r.created_at DESC',
        (device['name'],)
    )
    reports = cursor.fetchall()

    return render_template('device/view.html', device=device, reports=reports) 
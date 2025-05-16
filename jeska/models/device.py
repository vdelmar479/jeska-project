from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, send_file
)
from werkzeug.exceptions import abort
import json
from datetime import datetime
import io

from .auth import login_required
from .db import get_db

bp = Blueprint('device', __name__, url_prefix='/devices')

# Index - List all devices
@bp.route('/')
@login_required
def index():
    db = get_db()
    devices = db.execute(
        'SELECT d.id, d.name, d.description, d.status, d.components, d.peripherals, d.location, d.buying_timestamp'
        ' FROM devices d'
        ' ORDER BY d.buying_timestamp DESC'
    ).fetchall()
    return render_template('device/index.html', devices=devices)

# Create a device
@bp.route('/create', methods=('GET', 'POST'))
@login_required
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
            db = get_db()
            db.execute(
                'INSERT INTO devices (name, description, status, components, peripherals, location, buying_timestamp)'
                ' VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)',
                (name, description, status, components, peripherals, location)
            )
            db.commit()
            return redirect(url_for('device.index'))

    return render_template('device/create.html')

# Get a device
def get_device(id, check_author=True):
    device = get_db().execute(
        'SELECT d.id, d.name, d.description, d.status, d.components, d.peripherals, d.location, d.buying_timestamp'
        ' FROM devices d'
        ' WHERE d.id = ?',
        (id,)
    ).fetchone()

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
            db = get_db()
            db.execute(
                'UPDATE devices SET name = ?, description = ?, status = ?, components = ?, peripherals = ?, location = ?'
                ' WHERE id = ?',
                (name, description, status, components, peripherals, location, id)
            )
            db.commit()
            return redirect(url_for('device.index'))

    return render_template('device/update.html', device=device)

# Delete a device
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_device(id)
    db = get_db()
    db.execute('DELETE FROM devices WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('device.index'))

# Import/Export page
@bp.route('/import-export', methods=['GET'])
@login_required
def import_export():
    return render_template('device/import_export.html')

# Export all devices as JSON
@bp.route('/export', methods=['GET'])
@login_required
def export_devices():
    db = get_db()
    devices = db.execute(
        'SELECT d.id, d.name, d.description, d.status, d.components, d.peripherals, d.location, d.buying_timestamp'
        ' FROM devices d'
        ' ORDER BY d.buying_timestamp DESC'
    ).fetchall()
    
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
            'buying_timestamp': device['buying_timestamp']
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
        
        db = get_db()
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
                db.execute(
                    'INSERT OR REPLACE INTO devices (name, description, status, components, peripherals, location, buying_timestamp)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (
                        device['name'],
                        device.get('description', ''),
                        device.get('status', ''),
                        components,
                        peripherals,
                        device.get('location', ''),
                        device.get('buying_timestamp', datetime.now().isoformat())
                    )
                )
                imported_count += 1
                
            except Exception as e:
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
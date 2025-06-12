from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import mysql.connector
import json

from .auth import login_required, admin_required
from .db import get_db
from .. import config

bp = Blueprint('component', __name__, url_prefix='/components')

# Index - List all components
@bp.route('/')
@login_required
def index():
    db, cursor = get_db()
    cursor.execute(
        'SELECT c.id, c.name, c.type, c.description, c.in_use, c.total'
        ' FROM components c'
        ' ORDER BY c.name ASC'
    )
    components = cursor.fetchall()
    return render_template('component/index.html', components=components, config=config)

# Create a component
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
            error = 'Component name is required.'
        if not type:
            error = 'Component type is required.'
        if total < 0:
            error = 'Total quantity must be non-negative.'

        if error is not None:
            flash(error, 'danger')
        else:
            try:
                db, cursor = get_db()
                cursor.execute(
                    'INSERT INTO components (name, type, description, total, in_use)'
                    ' VALUES (%s, %s, %s, %s, 0)',
                    (name, type, description, total)
                )
                db.commit()
                flash('Component created successfully.', 'success')
                return redirect(url_for('component.index'))
            except mysql.connector.Error as e:
                if e.errno == 1062:  # Duplicate entry error
                    flash('Component name already exists.', 'danger')
                else:
                    flash('Database error occurred.', 'danger')
                return redirect(url_for('component.create'))

    return render_template('component/create.html')

# Get a component
def get_component(id):
    db, cursor = get_db()
    cursor.execute(
        'SELECT c.id, c.name, c.type, c.description, c.in_use, c.total'
        ' FROM components c'
        ' WHERE c.id = %s',
        (id,)
    )
    component = cursor.fetchone()

    if component is None:
        abort(404, f"Component id {id} doesn't exist.")

    return component

# Update a component
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
@admin_required
def update(id):
    component = get_component(id)

    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        description = request.form['description']
        total = request.form.get('total', 0, type=int)
        error = None

        if not name:
            error = 'Component name is required.'
        if not type:
            error = 'Component type is required.'
        if total < component['in_use']:
            error = 'Total quantity cannot be less than components in use.'

        if error is not None:
            flash(error, 'danger')
        else:
            try:
                db, cursor = get_db()
                cursor.execute(
                    'UPDATE components SET name = %s, type = %s, description = %s, total = %s'
                    ' WHERE id = %s',
                    (name, type, description, total, id)
                )
                db.commit()
                flash('Component updated successfully.', 'success')
                return redirect(url_for('component.index'))
            except mysql.connector.Error as e:
                if e.errno == 1062:  # Duplicate entry error
                    flash('Component name already exists.', 'danger')
                else:
                    flash('Database error occurred.', 'danger')
                return redirect(url_for('component.update', id=id))

    return render_template('component/update.html', component=component)

# Delete a component
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
@admin_required
def delete(id):
    component = get_component(id)
    if component['in_use'] > 0:
        flash('Cannot delete component that is currently in use.', 'danger')
        return redirect(url_for('component.index'))
        
    try:
        db, cursor = get_db()
        cursor.execute('DELETE FROM components WHERE id = %s', (id,))
        db.commit()
        flash('Component deleted successfully.', 'success')
        return redirect(url_for('component.index'))
    except mysql.connector.Error:
        flash('Error deleting component.', 'danger')
        return redirect(url_for('component.index'))

# API endpoints for AJAX operations
@bp.route('/api/component/<int:id>', methods=['GET'])
@login_required
def get_component_api(id):
    component = get_component(id)
    return jsonify({
        'id': component['id'],
        'name': component['name'],
        'type': component['type'],
        'description': component['description'],
        'in_use': component['in_use'],
        'total': component['total']
    })

@bp.route('/api/component/<int:id>', methods=['PUT'])
@login_required
@admin_required
def update_component_api(id):
    component = get_component(id)
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Component name is required.'}), 400
    if not data.get('type'):
        return jsonify({'error': 'Component type is required.'}), 400
    
    total = data.get('total', component['total'])
    if total < component['in_use']:
        return jsonify({'error': 'Total quantity cannot be less than components in use.'}), 400

    try:
        db, cursor = get_db()
        cursor.execute(
            'UPDATE components SET name = %s, type = %s, description = %s, total = %s'
            ' WHERE id = %s',
            (data['name'], data['type'], data.get('description', ''), total, id)
        )
        db.commit()
        
        return jsonify({
            'id': id,
            'name': data['name'],
            'type': data['type'],
            'description': data.get('description', ''),
            'in_use': component['in_use'],
            'total': total
        })
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry error
            return jsonify({'error': 'Component name already exists.'}), 400
        return jsonify({'error': 'Database error occurred.'}), 500

@bp.route('/api/component', methods=['POST'])
@login_required
@admin_required
def create_component_api():
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Component name is required.'}), 400
    if not data.get('type'):
        return jsonify({'error': 'Component type is required.'}), 400
    
    total = data.get('total', 0)
    if total < 0:
        return jsonify({'error': 'Total quantity must be non-negative.'}), 400

    try:
        db, cursor = get_db()
        cursor.execute(
            'INSERT INTO components (name, type, description, total, in_use)'
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
            return jsonify({'error': 'Component name already exists.'}), 400
        return jsonify({'error': 'Database error occurred.'}), 500

@bp.route('/consolidate', methods=['POST'])
@login_required
@admin_required
def consolidate_components():
    try:
        db, cursor = get_db()
        
        # Get all devices and their components
        cursor.execute(
            'SELECT components FROM devices'
        )
        devices = cursor.fetchall()
        
        # Create a dictionary to count component usage
        component_counts = {}
        
        # Count components across all devices
        for device in devices:
            if device['components']:
                components = device['components'].split(',')
                for component in components:
                    component = component.strip()
                    if component:
                        component_counts[component] = component_counts.get(component, 0) + 1
        
        # Update the in_use field for each component
        for component_name, count in component_counts.items():
            cursor.execute(
                'UPDATE components SET in_use = %s WHERE name = %s',
                (count, component_name)
            )
        
        # Reset in_use to 0 for components not found in any device
        if component_counts:
            # If we have components, use them in the NOT IN clause
            placeholders = ', '.join(['%s'] * len(component_counts))
            cursor.execute(
                f'UPDATE components SET in_use = 0 WHERE name NOT IN ({placeholders})',
                tuple(component_counts.keys())
            )
        else:
            # If no components found, reset all components
            cursor.execute('UPDATE components SET in_use = 0')
        
        db.commit()
        return jsonify({
            'message': 'Components consolidated successfully',
            'component_counts': component_counts
        }), 200
        
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error occurred: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@bp.route('/import', methods=['POST'])
def import_components():
    try:
        # Get the uploaded file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({'error': 'File must be a JSON file'}), 400

        # Read and parse JSON
        try:
            components_data = json.loads(file.read().decode('utf-8'))
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON format'}), 400

        # Validate required fields
        for component in components_data:
            if not all(key in component for key in ['name', 'type', 'total']):
                return jsonify({'error': 'Each component must have name, type, and total fields'}), 400

        db, cursor = get_db()
        imported = 0
        updated = 0
        errors = []

        for component in components_data:
            try:
                # Check if component exists
                cursor.execute(
                    'SELECT id FROM components WHERE name = %s',
                    (component['name'],)
                )
                existing = cursor.fetchone()

                if existing:
                    # Update existing component
                    cursor.execute(
                        'UPDATE components SET type = %s, description = %s, total = %s'
                        ' WHERE name = %s',
                        (component['type'], 
                         component.get('description', ''), 
                         component['total'],
                         component['name'])
                    )
                    updated += 1
                else:
                    # Insert new component
                    cursor.execute(
                        'INSERT INTO components (name, type, description, total, in_use)'
                        ' VALUES (%s, %s, %s, %s, 0)',
                        (component['name'],
                         component['type'],
                         component.get('description', ''),
                         component['total'])
                    )
                    imported += 1

            except mysql.connector.Error as e:
                if e.errno == 1062:  # Duplicate entry error
                    errors.append(f"Duplicate component name: {component['name']}")
                else:
                    errors.append(f"Error processing {component['name']}: {str(e)}")

        db.commit()

        return jsonify({
            'message': 'Import completed',
            'imported': imported,
            'updated': updated,
            'errors': errors
        }), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

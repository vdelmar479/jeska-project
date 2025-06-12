from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

from .auth import login_required
from .db import get_db
from .mail import EmailSender

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/list_devices', methods=['GET'])
def list_devices():
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
    
    return jsonify(devices_list)

@bp.route('/device/<int:device_id>', methods=['GET'])
def get_device(device_id):
    db, cursor = get_db()
    cursor.execute(
        'SELECT d.id, d.name, d.description, d.status, d.components, d.peripherals, d.location, d.buying_timestamp, d.mac_address'
        ' FROM devices d'
        ' WHERE d.id = %s',
        (device_id,)
    )
    device = cursor.fetchone()
    
    if device is None:
        abort(404, f"Device with id {device_id} doesn't exist.")
    
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
    
    return jsonify(device_dict)

@bp.route('/device', methods=['POST'])
@login_required
def create_device():
    if not request.is_json:
        abort(400, "Content-Type must be application/json")
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing required field: {field}")
    
    # Process components and peripherals lists
    components = ','.join(data.get('components', []))
    peripherals = ','.join(data.get('peripherals', []))
    
    try:
        db, cursor = get_db()
        cursor.execute(
            'INSERT INTO devices (name, description, status, components, peripherals, location, buying_timestamp, mac_address)'
            ' VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)',
            (data['name'], data.get('description', ''), data.get('status', 'Available'),
             components, peripherals, data.get('location', ''), data.get('mac_address', ''))
        )
        db.commit()
        
        # Return the created device
        return jsonify({
            'id': cursor.lastrowid,
            'name': data['name'],
            'description': data.get('description', ''),
            'status': data.get('status', 'Available'),
            'components': data.get('components', []),
            'peripherals': data.get('peripherals', []),
            'location': data.get('location', ''),
            'buying_timestamp': datetime.now().isoformat(),
            'mac_address': data.get('mac_address', '')
        }), 201
        
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry error
            abort(409, f"Device name '{data['name']}' already exists.")
        else:
            abort(500, "Database error occurred")

@bp.route('/device/<int:device_id>', methods=['PUT'])
@login_required
def update_device(device_id):
    if not request.is_json:
        abort(400, "Content-Type must be application/json")
    
    # Check if device exists
    db, cursor = get_db()
    cursor.execute('SELECT id FROM devices WHERE id = %s', (device_id,))
    device = cursor.fetchone()
    if device is None:
        abort(404, f"Device with id {device_id} doesn't exist.")
    
    data = request.get_json()
    
    # Process components and peripherals lists
    if 'components' in data:
        data['components'] = ','.join(data['components'])
    if 'peripherals' in data:
        data['peripherals'] = ','.join(data['peripherals'])
    
    # Build update query dynamically based on provided fields
    valid_fields = ['name', 'description', 'status', 'components', 'peripherals', 'location', 'mac_address']
    update_fields = []
    values = []
    
    for field in valid_fields:
        if field in data:
            update_fields.append(f"{field} = %s")
            values.append(data[field])
    
    if not update_fields:
        abort(400, "No valid fields to update")
    
    values.append(device_id)
    
    try:
        cursor.execute(
            f'UPDATE devices SET {", ".join(update_fields)} WHERE id = %s',
            values
        )
        db.commit()
        
        # Return updated device
        cursor.execute(
            'SELECT * FROM devices WHERE id = %s', (device_id,)
        )
        updated_device = cursor.fetchone()
        
        return jsonify({
            'id': updated_device['id'],
            'name': updated_device['name'],
            'description': updated_device['description'],
            'status': updated_device['status'],
            'components': updated_device['components'].split(',') if updated_device['components'] else [],
            'peripherals': updated_device['peripherals'].split(',') if updated_device['peripherals'] else [],
            'location': updated_device['location'],
            'buying_timestamp': updated_device['buying_timestamp'],
            'mac_address': updated_device['mac_address']
        })
        
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry error
            abort(409, f"Device name '{data.get('name')}' already exists.")
        else:
            abort(500, "Database error occurred")

@bp.route('/list_reports', methods=['GET'])
def list_reports():
    db, cursor = get_db()
    cursor.execute(
        'SELECT r.id, r.title, r.body, r.author_username, r.device_name, r.status, r.created_at'
        ' FROM reports r'
        ' ORDER BY r.created_at DESC'
    )
    reports = cursor.fetchall()
    
    # Convert reports to list of dictionaries
    reports_list = []
    for report in reports:
        report_dict = {
            'id': report['id'],
            'title': report['title'],
            'body': report['body'],
            'author_username': report['author_username'],
            'device_name': report['device_name'],
            'status': report['status'],
            'created_at': report['created_at']
        }
        reports_list.append(report_dict)
    
    return jsonify(reports_list)

@bp.route('/report/<int:report_id>', methods=['GET'])
def get_report(report_id):
    db, cursor = get_db()
    cursor.execute(
        'SELECT r.id, r.title, r.body, r.author_username, r.device_name, r.status, r.created_at'
        ' FROM reports r'
        ' WHERE r.id = %s',
        (report_id,)
    )
    report = cursor.fetchone()
    
    if report is None:
        abort(404, f"Report with id {report_id} doesn't exist.")
    
    report_dict = {
        'id': report['id'],
        'title': report['title'],
        'body': report['body'],
        'author_username': report['author_username'],
        'device_name': report['device_name'],
        'status': report['status'],
        'created_at': report['created_at']
    }
    
    return jsonify(report_dict)

@bp.route('/report', methods=['POST'])
@login_required
def create_report():
    if not request.is_json:
        abort(400, "Content-Type must be application/json")
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'device_name']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing required field: {field}")
    
    try:
        db, cursor = get_db()
        cursor.execute(
            'INSERT INTO reports (title, body, author_username, device_name, status, created_at)'
            ' VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)',
            (data['title'], data.get('body', ''), g.user['username'],
             data['device_name'], data.get('status', 'Open'))
        )
        db.commit()
        
        # Get admin users and send email notifications
        cursor.execute(
            'SELECT username, email FROM users WHERE role = %s',
            ('admin',)
        )
        admin_users = cursor.fetchall()
        
        if admin_users:
            # Create email sender
            email_sender = EmailSender()
            
            # Prepare email content
            subject = f"New Report Created: {data['title']}"
            body = f"""
A new report has been created:

Title: {data['title']}
Body:
{data.get('body', '(No content)')}
Device: {data['device_name']}
Author: {g.user['username']}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            # Send email to all admin users
            admin_emails = [user['email'] for user in admin_users]
            email_sender.send_email(
                to_emails=admin_emails,
                subject=subject,
                body=body
            )
        
        # Return the created report
        return jsonify({
            'id': cursor.lastrowid,
            'title': data['title'],
            'body': data.get('body', ''),
            'author_username': g.user['username'],
            'device_name': data['device_name'],
            'status': data.get('status', 'Open'),
            'created_at': datetime.now().isoformat()
        }), 201
        
    except mysql.connector.Error as e:
        if e.errno == 1452:  # Foreign key constraint error
            abort(409, f"Device '{data['device_name']}' doesn't exist.")
        else:
            abort(500, "Database error occurred")

@bp.route('/report/<int:report_id>', methods=['PUT'])
@login_required
def update_report(report_id):
    if not request.is_json:
        abort(400, "Content-Type must be application/json")
    
    # Check if report exists and user is the author
    db, cursor = get_db()
    cursor.execute('SELECT * FROM reports WHERE id = %s', (report_id,))
    report = cursor.fetchone()
    if report is None:
        abort(404, f"Report with id {report_id} doesn't exist.")
    
    data = request.get_json()
    
    # Build update query dynamically based on provided fields
    valid_fields = ['title', 'body', 'device_name', 'status']
    update_fields = []
    values = []
    
    for field in valid_fields:
        if field in data:
            update_fields.append(f"{field} = %s")
            values.append(data[field])
    
    if not update_fields:
        abort(400, "No valid fields to update")
    
    values.append(report_id)
    
    try:
        cursor.execute(
            f'UPDATE reports SET {", ".join(update_fields)} WHERE id = %s',
            values
        )
        db.commit()
        
        # Return updated report
        cursor.execute(
            'SELECT * FROM reports WHERE id = %s', (report_id,)
        )
        updated_report = cursor.fetchone()
        
        return jsonify({
            'id': updated_report['id'],
            'title': updated_report['title'],
            'body': updated_report['body'],
            'author_username': updated_report['author_username'],
            'device_name': updated_report['device_name'],
            'status': updated_report['status'],
            'created_at': updated_report['created_at']
        })
        
    except mysql.connector.Error as e:
        if e.errno == 1452:  # Foreign key constraint error
            abort(409, f"Device '{data.get('device_name')}' doesn't exist.")
        else:
            abort(500, "Database error occurred")

@bp.route('/list_devices_names', methods=['GET'])
def list_devices_names():
    db, cursor = get_db()
    cursor.execute(
        'SELECT name FROM devices ORDER BY name'
    )
    devices = cursor.fetchall()
    
    # Convert to list of names
    device_names = [device['name'] for device in devices]
    
    return jsonify(device_names)

@bp.route('/check_active_reports/<device_name>', methods=['GET'])
def check_active_reports(device_name):
    db, cursor = get_db()
    cursor.execute(
        'SELECT r.id, r.title, r.body, r.author_username, r.device_name, r.status, r.created_at'
        ' FROM reports r'
        ' WHERE r.device_name = %s AND r.status = %s'
        ' ORDER BY r.created_at DESC',
        (device_name, 'Open')
    )
    reports = cursor.fetchall()
    
    # Convert reports to list of dictionaries
    reports_list = []
    for report in reports:
        report_dict = {
            'id': report['id'],
            'title': report['title'],
            'body': report['body'],
            'author_username': report['author_username'],
            'device_name': report['device_name'],
            'status': report['status'],
            'created_at': report['created_at']
        }
        reports_list.append(report_dict)
    
    return jsonify(reports_list)

@bp.route('/update_profile', methods=['PUT'])
@login_required
def update_profile():
    if not request.is_json:
        abort(400, "Content-Type must be application/json")
    
    data = request.get_json()
    
    # Build update query dynamically based on provided fields
    valid_fields = ['name', 'surname', 'email']
    update_fields = []
    values = []
    
    for field in valid_fields:
        if field in data:
            update_fields.append(f"{field} = %s")
            values.append(data[field])
    
    if not update_fields:
        abort(400, "No valid fields to update")
    
    values.append(g.user['username'])
    
    try:
        db, cursor = get_db()
        cursor.execute(
            f'UPDATE users SET {", ".join(update_fields)} WHERE username = %s',
            values
        )
        db.commit()
        
        # Return updated user info
        cursor.execute(
            'SELECT username, name, surname, email, role FROM users WHERE username = %s',
            (g.user['username'],)
        )
        updated_user = cursor.fetchone()
        
        return jsonify({
            'username': updated_user['username'],
            'name': updated_user['name'],
            'surname': updated_user['surname'],
            'email': updated_user['email'],
            'role': updated_user['role']
        })
        
    except mysql.connector.Error:
        abort(500, "Database error occurred")

@bp.route('/change_password', methods=['PUT'])
@login_required
def change_password():
    if not request.is_json:
        abort(400, "Content-Type must be application/json")
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['current_password', 'new_password']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing required field: {field}")
    
    db, cursor = get_db()
    cursor.execute(
        'SELECT * FROM users WHERE username = %s', (g.user['username'],)
    )
    user = cursor.fetchone()
    
    # Verify current password
    if not check_password_hash(user['password'], data['current_password']):
        abort(401, "Current password is incorrect")
    
    # Update password
    try:
        cursor.execute(
            'UPDATE users SET password = %s WHERE username = %s',
            (generate_password_hash(data['new_password']), g.user['username'])
        )
        db.commit()
        return jsonify({'message': 'Password updated successfully'})
        
    except mysql.connector.Error:
        abort(500, "Database error occurred")

@bp.route('/recent_active_reports', methods=['GET'])
def get_recent_active_reports():
    db, cursor = get_db()
    cursor.execute(
        'SELECT r.id, r.title, r.device_name, r.status, r.created_at, r.author_username'
        ' FROM reports r'
        ' WHERE r.status = %s'
        ' ORDER BY r.created_at DESC'
        ' LIMIT 5',
        ('Open',)
    )
    reports = cursor.fetchall()
    
    # Convert reports to list of dictionaries
    reports_list = []
    for report in reports:
        report_dict = {
            'id': report['id'],
            'title': report['title'],
            'device_name': report['device_name'],
            'status': report['status'],
            'created_at': report['created_at'],
            'author_username': report['author_username']
        }
        reports_list.append(report_dict)
    
    return jsonify(reports_list)

@bp.route('/reports_last_seven_days', methods=['GET'])
def get_reports_last_seven_days():
    db, cursor = get_db()
    
    # Get reports count for each of the last 7 days
    cursor.execute('''
        WITH RECURSIVE dates(date) AS (
            SELECT DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            UNION ALL
            SELECT DATE_ADD(date, INTERVAL 1 DAY)
            FROM dates
            WHERE date < CURDATE()
        )
        SELECT 
            dates.date as report_date,
            COUNT(r.id) as report_count
        FROM dates
        LEFT JOIN reports r ON DATE(r.created_at) = dates.date
        GROUP BY dates.date
        ORDER BY dates.date
    ''')
    reports = cursor.fetchall()
    
    # Convert to list of dictionaries
    result = []
    for row in reports:
        result.append({
            'date': row['report_date'].isoformat(),
            'count': row['report_count']
        })
    
    return jsonify(result)

@bp.route('/devices_by_status', methods=['GET'])
def get_devices_by_status():
    db, cursor = get_db()
    
    # Get count of devices grouped by status
    cursor.execute('''
        SELECT 
            status,
            COUNT(*) as count
        FROM devices
        GROUP BY status
        ORDER BY status
    ''')
    devices = cursor.fetchall()
    
    # Convert to list of dictionaries
    result = []
    for row in devices:
        result.append({
            'status': row['status'],
            'count': row['count']
        })
    
    return jsonify(result)

@bp.route('/admin_users', methods=['GET'])
def get_admin_users():
    db, cursor = get_db()
    
    # Get all users with admin role
    cursor.execute('''
        SELECT username, email
        FROM users
        WHERE role = 'admin'
        ORDER BY username
    ''')
    admin_users = cursor.fetchall()
    
    # Convert to list of dictionaries
    result = []
    for user in admin_users:
        result.append({
            'username': user['username'],
            'email': user['email']
        })
    
    return jsonify(result)

@bp.route('/update_user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    if not request.is_json:
        abort(400, "Content-Type must be application/json")
    
    # Check if user has admin role
    if g.user['role'] != 'admin':
        abort(403, "You do not have permission to update users")
    
    data = request.get_json()
    
    # Build update query dynamically based on provided fields
    valid_fields = ['name', 'surname', 'email', 'role']
    update_fields = []
    values = []
    
    for field in valid_fields:
        if field in data:
            update_fields.append(f"{field} = %s")
            values.append(data[field])
    
    if not update_fields:
        abort(400, "No valid fields to update")
    
    values.append(user_id)
    
    try:
        db, cursor = get_db()
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        if user is None:
            abort(404, f"User with id {user_id} doesn't exist")
            
        cursor.execute(
            f'UPDATE users SET {", ".join(update_fields)} WHERE id = %s',
            values
        )
        db.commit()
        
        # Return updated user info
        cursor.execute(
            'SELECT id, username, name, surname, email, role FROM users WHERE id = %s',
            (user_id,)
        )
        updated_user = cursor.fetchone()
        
        return jsonify({
            'id': updated_user['id'],
            'username': updated_user['username'],
            'name': updated_user['name'],
            'surname': updated_user['surname'],
            'email': updated_user['email'],
            'role': updated_user['role']
        })
        
    except mysql.connector.Error:
        abort(500, "Database error occurred")

@bp.route('/component/<int:component_id>', methods=['GET'])
def get_component(component_id):
    db, cursor = get_db()
    cursor.execute(
        'SELECT c.id, c.name, c.type, c.description, c.in_use, c.total'
        ' FROM components c'
        ' WHERE c.id = %s',
        (component_id,)
    )
    component = cursor.fetchone()
    
    if component is None:
        abort(404, f"Component with id {component_id} doesn't exist.")
    
    return jsonify({
        'id': component['id'],
        'name': component['name'],
        'type': component['type'],
        'description': component['description'],
        'in_use': component['in_use'],
        'total': component['total']
    })

@bp.route('/component', methods=['POST'])
@login_required
def create_component():
    if not request.is_json:
        abort(400, "Content-Type must be application/json")
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'type']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing required field: {field}")
    
    try:
        db, cursor = get_db()
        cursor.execute(
            'INSERT INTO components (name, type, description, total, in_use)'
            ' VALUES (%s, %s, %s, %s, 0)',
            (data['name'], data['type'], data.get('description', ''), data.get('total', 0))
        )
        db.commit()
        
        # Return the created component
        return jsonify({
            'id': cursor.lastrowid,
            'name': data['name'],
            'type': data['type'],
            'description': data.get('description', ''),
            'total': data.get('total', 0),
            'in_use': 0
        }), 201
        
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry error
            abort(409, f"Component name '{data['name']}' already exists.")
        else:
            abort(500, "Database error occurred")

@bp.route('/component/<int:component_id>', methods=['PUT'])
@login_required
def update_component(component_id):
    if not request.is_json:
        abort(400, "Content-Type must be application/json")
    
    # Check if component exists
    db, cursor = get_db()
    cursor.execute(
        'SELECT id, in_use FROM components WHERE id = %s',
        (component_id,)
    )
    component = cursor.fetchone()
    
    if component is None:
        abort(404, f"Component with id {component_id} doesn't exist.")
    
    data = request.get_json()
    
    # Validate total vs in_use
    if 'total' in data and data['total'] < component['in_use']:
        abort(400, "Total quantity cannot be less than components in use.")
    
    # Build update query dynamically based on provided fields
    valid_fields = ['name', 'type', 'description', 'total']
    update_fields = []
    values = []
    
    for field in valid_fields:
        if field in data:
            update_fields.append(f"{field} = %s")
            values.append(data[field])
    
    if not update_fields:
        abort(400, "No valid fields to update")
    
    values.append(component_id)
    
    try:
        cursor.execute(
            f'UPDATE components SET {", ".join(update_fields)} WHERE id = %s',
            values
        )
        db.commit()
        
        # Return updated component
        cursor.execute(
            'SELECT * FROM components WHERE id = %s',
            (component_id,)
        )
        updated_component = cursor.fetchone()
        
        return jsonify({
            'id': updated_component['id'],
            'name': updated_component['name'],
            'type': updated_component['type'],
            'description': updated_component['description'],
            'in_use': updated_component['in_use'],
            'total': updated_component['total']
        })
        
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry error
            abort(409, f"Component name '{data.get('name')}' already exists.")
        else:
            abort(500, "Database error occurred")

@bp.route('/list_component_names', methods=['GET'])
def list_component_names():
    db, cursor = get_db()
    cursor.execute(
        'SELECT name FROM components ORDER BY name'
    )
    components = cursor.fetchall()
    
    # Convert to list of names
    component_names = [component['name'] for component in components]
    
    return jsonify(component_names)

@bp.route('/list_peripheral_names', methods=['GET'])
def list_peripheral_names():
    db, cursor = get_db()
    cursor.execute(
        'SELECT name FROM peripherals ORDER BY name'
    )
    peripherals = cursor.fetchall()
    
    # Convert to list of names
    peripheral_names = [peripheral['name'] for peripheral in peripherals]
    
    return jsonify(peripheral_names)

@bp.route('/device_id_by_name/<device_name>', methods=['GET'])
def get_device_id_by_name(device_name):
    db, cursor = get_db()
    cursor.execute(
        'SELECT id FROM devices WHERE name = %s',
        (device_name,)
    )
    device = cursor.fetchone()
    
    if device is None:
        abort(404, f"Device with name '{device_name}' doesn't exist.")
    
    return jsonify({'id': device['id']})

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import mysql.connector
import json
import os

from .auth import login_required, admin_required
from .db import get_db
from .. import config

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

def update_config_file(key, values):
    """Update a configuration list in config.py"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.py')
    
    with open(config_path, 'r') as f:
        lines = f.readlines()
    
    # Find the start and end of the list
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith(f'{key} = ['):
            start_idx = i
        elif start_idx is not None and line.strip().startswith(']'):
            end_idx = i
            break
    
    if start_idx is None or end_idx is None:
        return False
    
    # Create the new list content
    new_content = f'{key} = [\n'
    for value in values:
        new_content += f"    '{value}',\n"
    new_content += ']\n'
    
    # Replace the old list with the new one
    lines[start_idx:end_idx + 1] = new_content
    
    # Write back to the file
    with open(config_path, 'w') as f:
        f.writelines(lines)
    
    # Update the config module
    setattr(config, key, values)
    return True

# Index - List all configurations
@bp.route('/')
@login_required
@admin_required
def index():
    return render_template('configuration/index.html', config=config)

@bp.route('/update-locations', methods=['POST'])
@login_required
@admin_required
def update_locations():
    data = request.get_json()
    if update_config_file('LOCATIONS', data['values']):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@bp.route('/update-device-statuses', methods=['POST'])
@login_required
@admin_required
def update_device_statuses():
    data = request.get_json()
    if update_config_file('DEVICE_STATUSES', data['values']):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@bp.route('/update-report-statuses', methods=['POST'])
@login_required
@admin_required
def update_report_statuses():
    data = request.get_json()
    if update_config_file('REPORT_STATUSES', data['values']):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@bp.route('/update-component-types', methods=['POST'])
@login_required
@admin_required
def update_component_types():
    data = request.get_json()
    if update_config_file('COMPONENT_TYPES', data['values']):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@bp.route('/update-peripheral-types', methods=['POST'])
@login_required
@admin_required
def update_peripheral_types():
    data = request.get_json()
    if update_config_file('PERIPHERAL_TYPES', data['values']):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400
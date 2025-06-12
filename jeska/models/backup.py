from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, send_file, current_app
)
from werkzeug.exceptions import abort
import mysql.connector
import subprocess
import os
import tempfile
import datetime
import zipfile
import shutil
from pathlib import Path

from .auth import login_required, admin_required
from .db import get_db
from .. import config

bp = Blueprint('backup', __name__, url_prefix='/backup')

# XAMPP MySQL tools path
XAMPP_MYSQL_PATH = '/Applications/XAMPP/xamppfiles/bin'

def get_mysql_tool_path(tool_name):
    """Get the full path to a MySQL tool in XAMPP"""
    return os.path.join(XAMPP_MYSQL_PATH, tool_name)

def check_mysql_tools():
    """Check if XAMPP MySQL tools are installed and accessible"""
    mysqldump_path = get_mysql_tool_path('mysqldump')
    if not os.path.exists(mysqldump_path):
        return False
    try:
        # Try to get mysqldump version
        subprocess.run([mysqldump_path, '--version'], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_backup_file():
    """Create a backup file with timestamp in the name"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'backup_{timestamp}.sql'

def compress_file(input_path, output_path):
    """Compress a file using ZIP"""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_path, os.path.basename(input_path))

def decompress_file(input_path, output_path):
    """Decompress a ZIP file"""
    with zipfile.ZipFile(input_path, 'r') as zipf:
        # Extract the first file (should be our SQL file)
        sql_filename = zipf.namelist()[0]
        with zipf.open(sql_filename) as source, open(output_path, 'wb') as target:
            shutil.copyfileobj(source, target)

@bp.route('/')
@login_required
@admin_required
def index():
    # Check if MySQL tools are installed
    if not check_mysql_tools():
        flash('XAMPP MySQL tools not found. Please make sure XAMPP is installed at /Applications/XAMPP.', 'warning')
    return render_template('backup/index.html', config=config)

@bp.route('/export', methods=['GET'])
@login_required
@admin_required
def export_database():
    # Check if MySQL tools are installed
    if not check_mysql_tools():
        flash('XAMPP MySQL tools not found. Please make sure XAMPP is installed at /Applications/XAMPP.', 'danger')
        return redirect(url_for('backup.index'))

    try:
        # Create a temporary file for the SQL dump
        with tempfile.NamedTemporaryFile(suffix='.sql', delete=False) as temp_file:
            temp_path = temp_file.name

        # Get database configuration from hardcoded values
        db_config = {
            'user': 'root',
            'password': '',
            'host': '127.0.0.1',
            'port': '3307',
            'database': 'jeska'
        }
        
        # Get full path to mysqldump
        mysqldump_path = get_mysql_tool_path('mysqldump')
        
        # Construct mysqldump command
        mysqldump_cmd = [
            mysqldump_path,
            f'--user={db_config["user"]}',
            f'--password={db_config["password"]}',
            f'--host={db_config["host"]}',
            f'--port={db_config["port"]}',
            '--databases',
            db_config['database'],
            '--result-file=' + temp_path
        ]

        # Execute mysqldump
        subprocess.run(mysqldump_cmd, check=True)

        # Create a compressed version
        compressed_path = temp_path + '.zip'
        compress_file(temp_path, compressed_path)

        # Clean up the uncompressed file
        os.unlink(temp_path)

        # Send the compressed file
        return send_file(
            compressed_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        )

    except subprocess.CalledProcessError as e:
        flash('Error creating database backup: ' + str(e), 'danger')
        return redirect(url_for('backup.index'))
    except Exception as e:
        flash('Unexpected error during backup: ' + str(e), 'danger')
        return redirect(url_for('backup.index'))
    finally:
        # Clean up temporary files
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
        if 'compressed_path' in locals() and os.path.exists(compressed_path):
            os.unlink(compressed_path)

@bp.route('/import', methods=['POST'])
@login_required
@admin_required
def import_database():
    # Check if MySQL tools are installed
    if not check_mysql_tools():
        flash('XAMPP MySQL tools not found. Please make sure XAMPP is installed at /Applications/XAMPP.', 'danger')
        return redirect(url_for('backup.index'))

    if 'file' not in request.files:
        flash('No file provided', 'danger')
        return redirect(url_for('backup.index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('backup.index'))
    
    if not file.filename.endswith('.zip'):
        flash('File must be a ZIP backup file (.zip)', 'danger')
        return redirect(url_for('backup.index'))
    
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_compressed:
            temp_compressed_path = temp_compressed.name
            file.save(temp_compressed_path)

        with tempfile.NamedTemporaryFile(suffix='.sql', delete=False) as temp_sql:
            temp_sql_path = temp_sql.name

        # Decompress the file
        decompress_file(temp_compressed_path, temp_sql_path)

        # Get database configuration from hardcoded values
        db_config = {
            'user': 'root',
            'password': '',
            'host': '127.0.0.1',
            'port': '3307',
            'database': 'jeska'
        }

        # Get full path to mysql
        mysql_path = get_mysql_tool_path('mysql')

        # First, drop and recreate the database
        try:
            db, cursor = get_db()
            cursor.execute(f'DROP DATABASE IF EXISTS {db_config["database"]}')
            cursor.execute(f'CREATE DATABASE {db_config["database"]}')
            db.commit()
        except Exception as e:
            flash(f'Error preparing database: {str(e)}', 'danger')
            return redirect(url_for('backup.index'))

        # Construct mysql command for import
        mysql_cmd = [
            mysql_path,
            f'--user={db_config["user"]}',
            f'--password={db_config["password"]}',
            f'--host={db_config["host"]}',
            f'--port={db_config["port"]}',
            db_config['database']
        ]

        # Execute mysql import using subprocess.Popen to handle the input file
        with open(temp_sql_path, 'r') as sql_file:
            process = subprocess.Popen(
                mysql_cmd,
                stdin=sql_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, mysql_cmd, stderr)

        flash('Database restored successfully', 'success')
        return redirect(url_for('backup.index'))

    except subprocess.CalledProcessError as e:
        flash(f'Error restoring database: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))
    except Exception as e:
        flash(f'Unexpected error during restore: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))
    finally:
        # Clean up temporary files
        if 'temp_compressed_path' in locals() and os.path.exists(temp_compressed_path):
            os.unlink(temp_compressed_path)
        if 'temp_sql_path' in locals() and os.path.exists(temp_sql_path):
            os.unlink(temp_sql_path)
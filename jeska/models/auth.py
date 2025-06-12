import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register a user
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form.get('name', '')
        surname = request.form.get('surname', '')
        email = request.form.get('email', '')
        role = request.form.get('role', 'user')

        db, cursor = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                cursor.execute(
                    """INSERT INTO users (username, password, name, surname, email, role) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (username, generate_password_hash(password), name, surname, email, role),
                )
                db.commit()
            except mysql.connector.Error as e:
                if e.errno == 1062:  # Duplicate entry error
                    error = f"User {username} is already registered."
                else:
                    error = "Database error occurred."
            else:
                # Return JSON response for successful registration
                return {'ok': True, 'message': 'User registered successfully.'}, 200

        # Return JSON error response
        return {'ok': False, 'error': error}, 400

    # Only render the template for GET requests
    return redirect(url_for('index'))

# Login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    # if user already logged redirect to index
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, cursor = get_db()
        error = None
        
        cursor.execute(
            'SELECT * FROM users WHERE username = %s', (username,)
        )
        user = cursor.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# Checking if a session is started
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, cursor = get_db()
        cursor.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = cursor.fetchone()

# Log out
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Checking authentication
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# Profile page
@bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

# Admin role check decorator
def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user['role'] != 'admin':
            flash('You do not have permission to access this page.')
            return redirect(url_for('index'))
        return view(**kwargs)
    return wrapped_view

# List users (admin only)
@bp.route('/users')
@login_required
@admin_required
def list_users():
    db, cursor = get_db()
    cursor.execute('SELECT id, username, name, surname, email, role FROM users')
    users = cursor.fetchall()
    return render_template('auth/users.html', users=users)

# Delete user (admin only)
@bp.route('/users/<int:user_id>/delete', methods=('POST',))
@login_required
@admin_required
def delete_user(user_id):
    # Additional security check
    if g.user['role'] != 'admin':
        flash('You do not have permission to delete users.')
        return redirect(url_for('index'))

    db, cursor = get_db()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        flash('User not found.')
        return redirect(url_for('auth.list_users'))
    
    # Prevent admin from deleting themselves
    if user_id == g.user['id']:
        flash('You cannot delete your own account.')
        return redirect(url_for('auth.list_users'))

    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    db.commit()
    flash('User deleted successfully!')
    return redirect(url_for('auth.list_users'))

# Reset user password (admin only)
@bp.route('/api/reset_password/<int:user_id>', methods=('PUT',))
@login_required
@admin_required
def reset_password(user_id):
    if g.user['role'] != 'admin':
        return {'ok': False, 'error': 'You do not have permission to reset passwords.'}, 403

    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return {'ok': False, 'error': 'New password is required.'}, 400

    db, cursor = get_db()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        return {'ok': False, 'error': 'User not found.'}, 404

    try:
        cursor.execute(
            'UPDATE users SET password = %s WHERE id = %s',
            (generate_password_hash(new_password), user_id)
        )
        db.commit()
        return {'ok': True, 'message': 'Password reset successfully.'}, 200
    except Exception as e:
        return {'ok': False, 'error': 'Error resetting password.'}, 500 
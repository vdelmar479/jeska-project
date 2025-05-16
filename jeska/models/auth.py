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
        
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    """INSERT INTO users (username, password, name, surname, email, role) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (username, generate_password_hash(password), name, surname, email, role),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

# Login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    # if user already logged redirect to index
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

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
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

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

# Update profile
@bp.route('/profile/update', methods=('GET', 'POST'))
@login_required
def update_profile():
    if request.method == 'POST':
        name = request.form.get('name', '')
        surname = request.form.get('surname', '')
        email = request.form.get('email', '')
        error = None

        if error is None:
            db = get_db()
            db.execute(
                'UPDATE users SET name = ?, surname = ?, email = ? WHERE id = ?',
                (name, surname, email, g.user['id'])
            )
            db.commit()
            flash('Profile updated successfully!')
            return redirect(url_for('auth.profile'))

        flash(error)

    return render_template('auth/update_profile.html')

# Change password
@bp.route('/profile/change-password', methods=('GET', 'POST'))
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        error = None

        if not current_password:
            error = 'Current password is required.'
        elif not new_password:
            error = 'New password is required.'
        elif not confirm_password:
            error = 'Please confirm your new password.'
        elif new_password != confirm_password:
            error = 'New passwords do not match.'
        elif not check_password_hash(g.user['password'], current_password):
            error = 'Current password is incorrect.'

        if error is None:
            db = get_db()
            db.execute(
                'UPDATE users SET password = ? WHERE id = ?',
                (generate_password_hash(new_password), g.user['id'])
            )
            db.commit()
            flash('Password updated successfully!')
            return redirect(url_for('auth.profile'))

        flash(error)

    return render_template('auth/change_password.html')

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
    db = get_db()
    users = db.execute('SELECT id, username, name, surname, email, role FROM users').fetchall()
    return render_template('auth/users.html', users=users)

# Edit user (admin only)
@bp.route('/users/<int:user_id>/edit', methods=('GET', 'POST'))
@login_required
@admin_required
def edit_user(user_id):
    # Additional security check
    if g.user['role'] != 'admin':
        flash('You do not have permission to edit users.')
        return redirect(url_for('index'))

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if user is None:
        flash('User not found.')
        return redirect(url_for('auth.list_users'))

    if request.method == 'POST':
        name = request.form.get('name', '')
        surname = request.form.get('surname', '')
        email = request.form.get('email', '')
        role = request.form.get('role', 'user')
        error = None

        if error is None:
            db.execute(
                'UPDATE users SET name = ?, surname = ?, email = ?, role = ? WHERE id = ?',
                (name, surname, email, role, user_id)
            )
            db.commit()
            flash('User updated successfully!')
            return redirect(url_for('auth.list_users'))

        flash(error)

    return render_template('auth/edit_user.html', user=user)

# Delete user (admin only)
@bp.route('/users/<int:user_id>/delete', methods=('POST',))
@login_required
@admin_required
def delete_user(user_id):
    # Additional security check
    if g.user['role'] != 'admin':
        flash('You do not have permission to delete users.')
        return redirect(url_for('index'))

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if user is None:
        flash('User not found.')
        return redirect(url_for('auth.list_users'))
    
    # Prevent admin from deleting themselves
    if user_id == g.user['id']:
        flash('You cannot delete your own account.')
        return redirect(url_for('auth.list_users'))

    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    flash('User deleted successfully!')
    return redirect(url_for('auth.list_users')) 
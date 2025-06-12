import os

from flask import Flask, render_template, redirect, url_for, g
from .models.auth import login_required
from .models import db, auth, device, component, peripheral, report, configuration, backup, api
from .models.db import get_db
from . import config

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEV=True  # Adding DEV configuration
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Adding db functions to the application
    db.init_app(app)

    # Registering the auth blueprint to the factory
    app.register_blueprint(auth.bp)

    # Registering the device blueprint to the factory
    app.register_blueprint(device.bp)

    # Registering the component blueprint to the factory
    app.register_blueprint(component.bp)

    # Registering the component blueprint to the factory
    app.register_blueprint(peripheral.bp)

    # Registering the report blueprint to the factory
    app.register_blueprint(report.bp)

    # Registering the configuration blueprint to the factory
    app.register_blueprint(configuration.bp)

    # Registering the backup blueprint to the factory
    app.register_blueprint(backup.bp)

    # Registering the API blueprint to the factory
    app.register_blueprint(api.bp)

    # Main index route - serves as dashboard
    @app.route('/')
    @login_required
    def index():
        # Get user role
        db, cursor = get_db()
        cursor.execute(
            'SELECT role FROM users WHERE username = %s',
            (g.user['username'],)
        )
        user = cursor.fetchone()
        
        is_admin = user['role'] == 'admin' if user and user['role'] else False
        
        return render_template('dashboard/index.html', is_admin=is_admin, config=config)

    return app
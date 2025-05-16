import os

from flask import Flask, render_template, redirect, url_for
from .models.auth import login_required

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'jeska.sqlite'),
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
    from .models import db
    db.init_app(app)

    # Registering the auth blueprint to the factory
    from .models import auth
    app.register_blueprint(auth.bp)

    # Registering the device blueprint to the factory
    from .models import device
    app.register_blueprint(device.bp)

    # Registering the report blueprint to the factory
    from .models import report
    app.register_blueprint(report.bp)

    # Main index route - serves as dashboard
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    return app
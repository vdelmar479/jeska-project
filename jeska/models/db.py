import mysql.connector
from datetime import datetime

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host='127.0.0.1',
            port=3307,
            user='root',
            password='',
            database='jeska'
        )
        g.cursor = g.db.cursor(dictionary=True)  # Use dictionary cursor for named columns

    return g.db, g.cursor


def close_db(e=None):
    cursor = g.pop('cursor', None)
    db = g.pop('db', None)

    if cursor is not None:
        cursor.close()
    if db is not None:
        db.close()

def init_db():
    db, cursor = get_db()

    with current_app.open_resource('schema.sql') as f:
        # Split the SQL file into individual statements
        sql_commands = f.read().decode('utf8').split(';')
        
        # Execute each statement
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
        
        db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# Adding db functions to the application
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command) 
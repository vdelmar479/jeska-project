from jeska import create_app
import os
import sys

app = create_app()

if __name__ == '__main__':
    # Set the Python executable path for the reloader
    os.environ['PYTHONPATH'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Disable reloader in debug mode when running under PyCharm
    is_pycharm = "PYCHARM_HOSTED" in os.environ
    
    app.run(
        host='127.0.0.1',
        port=6969,
        debug=app.config['DEV'],
        use_reloader=not is_pycharm  # Disable reloader when running in PyCharm
    )
    #app.run(host='127.0.0.1', port=8095, debug=True)
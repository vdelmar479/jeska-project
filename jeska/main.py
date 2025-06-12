from jeska import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6969, debug=app.config['DEV'])
    #app.run(host='127.0.0.1', port=8095, debug=True)
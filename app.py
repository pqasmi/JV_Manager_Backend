from flask import Flask, jsonify

import models

DEBUG=True

PORT=8000

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/test')
def get_list():
    return jsonify(['hello', 'hi', 'hey'])


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

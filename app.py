from flask import Flask, jsonify

import models

# import our package for handling cors
from flask_cors import CORS

from resources.jv import jv # import blueprint from resources.dogs

DEBUG=True

PORT=8000

app = Flask(__name__)

CORS(jv, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(jv, url_prefix='')

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

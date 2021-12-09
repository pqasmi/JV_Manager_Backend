from flask import Flask, jsonify

import models

# import our package for handling cors
from flask_cors import CORS
from resources.jv import jv # import blueprint from resources.jv
from resources.users import users
from flask_login import LoginManager

import os

DEBUG=True

PORT=8000

app = Flask(__name__)

# configure the LoginManager. According to this:
# https://flask-login.readthedocs.io/en/latest/#configuring-your-application
# we need to do several things

# 1. set up a secret/key for sessions
# as demonstrated here: https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions
app.secret_key = "1234567"

# 2. instantiate the LoginManager to actually get a login_manager
login_manager = LoginManager()

# 3. actually connect the app with the login_manager
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)
        return user
    except models.DoesNotExist:
        return None 

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(
        data={
            'error': 'User not logged in'
        },
        message="You must be logged in to access that resource",
        status=401
    ), 401


CORS(app, resources={r"/jv*": {"origins":['http://localhost:3000']}}, supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(jv, url_prefix='/jv')
app.register_blueprint(users, url_prefix='/users')

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

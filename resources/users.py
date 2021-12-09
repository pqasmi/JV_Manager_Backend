# this is like a "user controller" or maybe "auth controller" in Unit 2
import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash

from playhouse.shortcuts import model_to_dict

from flask_login import login_user, current_user, logout_user

# make this a blueprint
users = Blueprint('users', 'users')


@users.route('/', methods=['GET'])
def test_user_resource():
    return "user resource works"

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(
            data={},
            message=f"A user with the email {payload['email']} already exists",
            status=401
        ), 401 
    except models.DoesNotExist: 
        pw_hash = generate_password_hash(payload['password'])
        created_user = models.User.create(
            username=payload['username'],
            email=payload['email'],
            password=pw_hash
        )

        login_user(created_user)
        
        created_user_dict = model_to_dict(created_user)

        # we can't jsonify the password (generate_password_hash gives us something in type "bytes" which is unserializable)
        # plus we shouldn't be send back the encrypted pw anyways
        # print(type(created_user_dict['password']))
        # so let's just get rid of it
        created_user_dict.pop('password')
        return jsonify(
            data=created_user_dict,
            message=f"Successfully registered user{created_user_dict['email']}",
            status=201
        ), 201

@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()

    # look up the user by email
    try:
        user = models.User.get(models.User.email == payload['email'])

        user_dict = model_to_dict(user)

        password_is_good = check_password_hash(user_dict['password'], payload['password'])
  
        if (password_is_good):
            # LOG THE USER IN!!! using Flask-Login
            login_user(user) # in express we did this manually by setting stuff in session

            # respond --- all good -- remove the pw first
            user_dict.pop('password')

            return jsonify(
                data=user_dict,
                message=f"Successfully logged in {user_dict['email']}",
                status=200
            ), 200
        else:
            print("email is no good")
            return jsonify(
                data={},
                message="Email or password is incorrect", # let's be vague
                status=401
            ), 401 

    except models.DoesNotExist:
    # else if they don't exist
        print('email not found')
        # respond -- bad username or password
        return jsonify(
            data={},
            message="Email or password is incorrect", # let's be vague
            status=401
        ), 401 


@users.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():
    # https://flask-login.readthedocs.io/en/latest/#flask_login.current_user
    # we can access current_user because we called login_user and set up user_loader
    print(current_user)
    print(type(current_user)) # <class 'werkzeug.local.LocalProxy'> # google it if you're interested
 
     # you can tell whether a user is logged in using
     # current_user.is_authenticated (search in the docs)

    if not current_user.is_authenticated:
        return jsonify(
            data={},
            message="No user is currently logged in",
            status=401,
        ), 401
    else:
        print(f"{current_user.username} is current_user.name in GET logged_in_user")
        user_dict = model_to_dict(current_user)
        user_dict.pop('password')

        # OBSERVE -- YOU now have access to the currently logged in user
        # anywhere you want user current_user
        # also observe -- with flask_login, it will remember who is logged in
        # EVEN IF THE SERVER RESTARTS (unlike express/nodemon)
        return jsonify(
            data=user_dict,
            message=f"Currently logged in as {user_dict['email']}.",
            status=200
        ), 200



@users.route('/logout', methods=['GET'])
def logout():
    # following the logout here: https://flask-login.readthedocs.io/en/latest/#login-example
    logout_user()
    return jsonify(
        data={},
        message="Successfully logged out.",
        status=200
    ), 200 

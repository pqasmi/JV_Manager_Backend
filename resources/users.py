# this is like a "user controller" or maybe "auth controller" in Unit 2
import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

from playhouse.shortcuts import model_to_dict

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
            message="A user with that email already exists",
            status=401
        ), 401 
    except models.DoesNotExist: 
        pw_hash = generate_password_hash(payload['password'])
        created_user = models.User.create(
            username=payload['username'],
            email=payload['email'],
            password=pw_hash
        )

        created_user_dict = model_to_dict(created_user)

        # we can't jsonify the password (generate_password_hash gives us something in type "bytes" which is unserializable)
        # plus we shouldn't be send back the encrypted pw anyways
        # print(type(created_user_dict['password']))
        # so let's just get rid of it
        created_user_dict.pop('password')
        return jsonify(
            data=created_user_dict,
            message="Successfully registered user",
            status=201
        ), 201
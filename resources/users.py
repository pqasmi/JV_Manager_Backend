# this is like a "user controller" or maybe "auth controller" in Unit 2
import models

from flask import Blueprint, request

# make this a blueprint
users = Blueprint('users', 'users')


@users.route('/', methods=['GET'])
def test_user_resource():
    return "user resource works"

@users.route('/register', methods=['POST'])
def register():
    # this interm step analogous to making sure we can log req.body in express
    # note: we had to send JSON from postman (choose raw, select JSON from the drop menu, type a perfect JSON object with double quotes around keys)
    print(request.get_json())
    return "check terminal"
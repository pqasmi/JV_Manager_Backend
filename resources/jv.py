import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

# creating our blueprint
# first argument is the blueprint's name
# second arg is its import_name (from app.py line 13)
# similar to creating a router in express
# this is like a controller in express

jv = Blueprint('jv', 'jv')

@jv.route('/', methods=['GET'])
@login_required
def jv_index():
    result = models.Jv.select()
     # or use a list comprehension
    current_user_jv_dicts = [model_to_dict(jv) for jv in current_user.jv]

    for jv_dict in current_user_jv_dicts:
        jv_dict['preparer'].pop('password')

    return jsonify({
        'data': current_user_jv_dicts,
        'message': f"Successfully found {len(current_user_jv_dicts)} JV",
        'status': 200
    }), 200


@jv.route('/', methods=['POST'])
@login_required
def create_jv():
    # .get_json() attached to the request will extract JSON from the request body
    payload = request.get_json() # this is like req.body in express
    new_jv = models.Jv.create(name=payload['name'], logo=payload['logo'], location=payload['location'], ownership=payload['ownership'], sales=payload['sales'], preparer=current_user.id)

    print(new_jv)
    jv_dict = model_to_dict(new_jv)
    jv_dict['preparer'].pop('password')
    
    return jsonify(
        data=jv_dict,
        message='Successfully created JV!',
        status=201
    ), 201

# SHOW ROUTE
# GET /<jv_id>
# in express it looked something like this
# router.get('/:id')

@jv.route('/<id>', methods=['GET'])
def get_one_dogs(id):
    jv = models.Jv.get_by_id(id)
    print(jv)
    return jsonify(
        data = model_to_dict(jv),
        message = 'Success!!!! 🎉',
        status = 200
    ), 200

# PUT UPDATE ROUTE
# PUT /<id>
@jv.route('/<id>', methods=['PUT'])
@login_required
def update_jv(id):
    payload = request.get_json()
    models.Jv.update(**payload).where(models.Jv.id == id).execute()
    return jsonify(
        data = model_to_dict(models.Jv.get_by_id(id)),
        message = 'resource updated successfully',
        status = 200,
    ), 200

# DELETE/ DESTROY
# DELETE api/v1/dogs/<id>
@jv.route('/<id>', methods=['DELETE'])
@login_required
def delete_jv(id):
    # we are trying to delete the dog with the id that comes through as a param
    # check here for how: http://docs.peewee-orm.com/en/latest/peewee/querying.html#deleting-records
    delete_query = models.Jv.delete().where(models.Jv.id == id)
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)

    # todo: write logic -- if no rows were deleted return
    # some message that tells that the delete did not happen

    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} jv with id {id}",
        status=200
    ), 200
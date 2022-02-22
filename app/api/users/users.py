from app.api import bp
from flasgger import swag_from
from flask import jsonify, request, Response
from marshmallow import ValidationError
from app.schemas import UserSchema, PasswordSchema
from app.models import Tag, Role
from app.api.errors import bad_request
# from app.swagger.user_specs import post_spec
from app import db
from app.api.users.service import register, log_in, user_list, basic_auth, token_auth, remove_user, add_user, confirm_user
from datetime import datetime
from flask import Response
from app.models import User
from flask import abort
from app.swagger.user_specs import get_spec, post_spec, put_spec, token_spec, pass_spec, delete_spec, login_spec, act_spec
from app.api.errors import bad_request
from app.utils.helpers import build_page


@bp.route('/users', methods=['GET'])
@token_auth.login_required(role=[Role.Admin])
@swag_from(get_spec)
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', "")
    order = request.args.get('order', "asc")
    users = user_list(order_by, order).paginate(page, per_page, False)

    user_schema = UserSchema(many=True)
    return jsonify(build_page(user_schema, users, order_by, order))


@bp.route('/users/login', methods=['GET'])
@basic_auth.login_required
@swag_from(login_spec)
def login():
    user = basic_auth.current_user()
    user_schema = UserSchema()
    if(not user.active):
        return bad_request(f'Inactive account. Check your email for activation link')
    return jsonify(user_schema.dump(user))


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required(role=[Role.Admin])
@swag_from(delete_spec)
def delete_users(id):
    if(remove_user(id)):
        return Response(status=200)
    return bad_request(f'User with id={id} does not exist')


@bp.route('/users', methods=['POST'])
@token_auth.login_required(role=[Role.Admin])
@swag_from(post_spec)
def create_user():
    data = request.get_json() or {}
    user_schema = UserSchema()

    try:
        user = user_schema.load(
            data, transient=True)
        if(not add_user(user)):
            return bad_request('Error sending email')

    except ValidationError as err:
        print("error")
        return bad_request(err.messages)

    return jsonify(user_schema.dump(user))


@bp.route('/users/activate/<token>', methods=['POST'])
@swag_from(act_spec)
def activate_user(token):
    data = request.get_json() or {}
    if(not 'password' in data):
        return bad_request('Password is required')
    if(not 'username' in data):
        return bad_request('Username is required')
    if(len(data['password']) < 8 or len(data['password']) > 20):
        return bad_request('Invalid password. Min length:8, Max length:20')
    user = confirm_user(token, data['username'], data['password'])
    if(not user):
        return bad_request('Invalid activation token')

    return Response(status=200)


@bp.route('/users/token', methods=['POST'])
@basic_auth.login_required
@swag_from(token_spec)
def get_token():
    user = basic_auth.current_user()
    if(not user.active):
        return bad_request(f'Inactive account. Check your email for activation link')
    token = user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@bp.route('/users/<int:id>', methods=['PUT'])
@swag_from(put_spec)
@token_auth.login_required
def edit_user(id):
    if (not token_auth.current_user()) or token_auth.current_user().id != id:
        return Response(status=403)

    data = request.get_json()
    user_schema = UserSchema()
    user = User.query.get(id)
    if(user):
        data['id'] = user.id
    else:
        bad_request(f'User with id={id} does not exist')

    try:
        user = user_schema.load(
            data, session=db.session)
        db.session.add(user)
        db.session.commit()

    except ValidationError as err:
        print("error")
        return bad_request(err.messages)

    return jsonify(user_schema.dump(user))


@bp.route('/users/password', methods=['PUT'])
@swag_from(pass_spec)
@token_auth.login_required
def change_password():

    user = token_auth.current_user()
    data = request.get_json()

    pass_schema = PasswordSchema()
    pass_change = pass_schema.load(data)
    if(len(data['password']) < 8 or len(data['password']) > 20):
        return bad_request('Invalid password. Min length:8, Max length:20')

    if(user.check_password(pass_change['old_password'])):
        user.set_password(pass_change['password'])
    else:
        return bad_request(f'Old password is incorrect')

    return Response(status=200)

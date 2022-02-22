
from app import db
from app.models import User, Role
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.api.errors import error_response
from app.utils.helpers import generate_password, generate_confirmation_token, confirm_token
from app import mail
from flask_mail import Message
from flask import render_template
from app.utils.helpers import generate_order_by

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


def add_user(user):
    auto_pass = generate_password()
    user.set_password(auto_pass)
    token = generate_confirmation_token(user.email)
    try:
        send_activation_email(user.email, token)
    except Exception as e:
        print(e)
        return False
    db.session.add(user)
    db.session.commit()
    return True


def confirm_user(token, username, password):
    email = confirm_token(token)
    if(not email):
        return None
    user = User.query.filter_by(email=email).first()
    if(not user):
        return None
    user.username = username
    user.set_password(password)
    user.active = True
    db.session.commit()
    return user


def send_activation_email(email, token):
    msg = Message('Activation Email', sender='tranckandtrace@outlook.com',
                  recipients=[email])
    # activation_link = f'http://161.35.99.28:3000/account/activate/{token}'
    activation_link = f'http://134.209.221.84/account/activate/{token}'
    msg.body = f'Please, set password for your account throw this link: {activation_link}'
    msg.html = render_template(
        'activation template.html', link=activation_link)
    mail.send(msg)


def register(user, password):
    user.set_password(password)
    db.session.commit()


def log_in():
    pass


def user_list(order_by, order):
    result = User.query.filter(User.role != Role.Admin)
    if order_by:
        result = generate_order_by(result, User, order_by, order)
    return result


def remove_user(id):
    user = User.query.get(id)
    if(user and user.role != Role.Admin):
        db.session.delete(user)
        db.session.commit()
        return True
    return False


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)


@token_auth.get_user_roles
def get_user_roles(user):
    return [user.role]

from flasgger import swag_from
from flask import request
from app.models import Tag
from app.api.errors import bad_request
import flask_excel as excel
from flask import Response
from app.api.utility.service import get_xls, get_pdf
from app.api.errors import bad_request
from app.api import bp
from app.swagger.utility_specs import post_spec
from app import mail
from flask_mail import Message


@bp.route('/utility/convert', methods=['POST'])
@swag_from(post_spec)
def convert():
    format = request.args.get('format')
    data = request.get_json()
    if(format == 'xls'):
        return get_xls(data['table'], data['title'])
    if(format == 'pdf'):
        return get_pdf(data['table'], data['title'])
    return bad_request(f'Format must be pdf or xls')


@bp.route('/utility/email', methods=['POST'])
# @swag_from(post_spec)
def send_email():
    msg = Message('Hello', sender='example@gmail.com',
                  recipients=['rec@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return "Sent"

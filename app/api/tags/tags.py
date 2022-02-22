from app.api import bp
from flasgger import swag_from
from flask import jsonify, request, send_file, make_response
from marshmallow import ValidationError
from app.schemas import TagSchema, TagConfigSchema, ZoneEntrySchema, PositionSchema
from app.models import Tag
from app.api.errors import bad_request
from app.swagger.tags_specs import get_spec, post_spec, get_history_spec, get_position_spec, post_active_spec
from app import db
from app.api.tags.service import tag_list, zone_history, positions_history, activate
from datetime import datetime
import flask_excel as excel
from flask import Response
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.lib.pagesizes import letter
from io import StringIO, BytesIO
from app.api.users.service import token_auth
from dateutil import parser
from app.utils.helpers import build_page


@bp.route('/tags', methods=['GET'])
@swag_from(get_spec)
def get_tags():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', "")
    order = request.args.get('order', "asc")
    tags = tag_list(order_by, order).paginate(page, per_page, False)
    tag_schema = TagSchema(many=True)
    return jsonify(build_page(tag_schema, tags, order_by, order))


@bp.route('/tags/<id>', methods=['POST'])
@swag_from(post_spec)
@token_auth.login_required
def set_config(id):
    data = request.get_json()
    tag_config_schema = TagConfigSchema()
    tag_schema = TagSchema()
    tag = Tag.query.get(id)
    if(tag and tag.config):
        data['id'] = tag.config.id
    if(not tag):
        return bad_request(f'Tag with id={id} does not exist')
    try:
        config = tag_config_schema.load(
            data, session=db.session)
        config.tag = tag
        db.session.commit()

    except ValidationError as err:
        print("error")
        return bad_request(err.messages)

    return jsonify(tag_schema.dump(tag))


@bp.route('/tags/<id>', methods=['GET'])
@swag_from(get_history_spec)
def get_zone_history(id):
    tag = Tag.query.get(id)
    if(not tag):
        return bad_request(f'Tag with id={id} does not exist')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', "")
    order = request.args.get('order', "asc")
    history_pagination = zone_history(
        id, order_by, order).paginate(page, per_page, False)
    zone_entry_schema = ZoneEntrySchema(many=True)

    return jsonify(build_page(zone_entry_schema, history_pagination, order_by, order))


@bp.route('/tags/positions/<id>', methods=['GET'])
@swag_from(get_position_spec)
def get_positions(id):
    tag = Tag.query.get(id)
    if(not tag):
        return bad_request(f'Tag with id={id} does not exist')

    try:
        start_date = parser.parse(
            request.args.get("start_date"))
        end_date = parser.parse(
            request.args.get("end_date"))
    except:
        return bad_request(f'Bad date format')

    count = request.args.get('count', 10, type=int)
    if(count > 1000):
        return bad_request(f'Maximum count is 1000')

    history = positions_history(id, start_date, end_date, count)
    position_schema = PositionSchema(many=True)
    return jsonify(position_schema.dump(history))


@bp.route('/tags/activate/<id>', methods=['POST'])
@token_auth.login_required
@swag_from(post_active_spec)
def activate_tag(id):
    active = True if request.args.get('active') == 'true' else False
    tag = activate(id, active)
    if(not tag):
        return bad_request(f'Tag with id={id} does not exist')
    tag_schema = TagSchema()
    return jsonify(tag_schema.dump(tag))

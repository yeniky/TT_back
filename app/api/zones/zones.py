from app.api import bp
from flasgger import swag_from
from flask import jsonify, request
from marshmallow import ValidationError
from app.schemas import ZoneSchema, ZoneEntrySchema
from app.api.zones.service import zone_list, zone_history, deactivate
from app.api.errors import bad_request
from app.swagger.zones_specs import get_spec, post_spec, put_spec, get_history_spec, post_deactive_spec
from app import db
from app.models import Zone
from app.api.users.service import token_auth
from app.utils.helpers import build_page


@bp.route('/zones', methods=['GET'])
@swag_from(get_spec)
def get_zones():
    zones = zone_list()
    zone_schema = ZoneSchema(many=True)
    return jsonify(zone_schema.dump(zones))


@bp.route('/zones', methods=['POST'])
@swag_from(post_spec)
@token_auth.login_required
def create_zone():
    data = request.get_json()
    zone_schema = ZoneSchema()

    try:
        zone = zone_schema.load(
            data, session=db.session)
        print(zone)
        db.session.add(zone)
        db.session.commit()

    except ValidationError as err:
        print("error")
        return bad_request(err.messages)

    return jsonify(zone_schema.dump(zone))


@bp.route('/zones/<id>', methods=['PUT'])
@swag_from(put_spec)
@token_auth.login_required
def edit_zone(id):
    data = request.get_json()
    zone_schema = ZoneSchema()
    zone = Zone.query.get(id)
    if(zone):
        data['id'] = zone.id
    else:
        bad_request(f'Zone with id={id} does not exist')

    try:
        zone = zone_schema.load(
            data, session=db.session)
        db.session.add(zone)
        db.session.commit()

    except ValidationError as err:
        print("error")
        return bad_request(err.messages)

    return jsonify(zone_schema.dump(zone))


@bp.route('/zones/<id>', methods=['GET'])
@swag_from(get_history_spec)
def get_history(id):
    zone = Zone.query.get(id)
    if(not zone):
        return bad_request(f'Zone with id={id} does not exist')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', "")
    order = request.args.get('order', "asc")

    history = zone_history(id, order_by, order).paginate(page, per_page, False)
    zone_entry_schema = ZoneEntrySchema(many=True)

    return jsonify(build_page(zone_entry_schema, history, order_by, order))


@bp.route('/zones/deactivate/<id>', methods=['POST'])
@swag_from(post_deactive_spec)
@token_auth.login_required
def deactivate_zone(id):
    zone = deactivate(id)
    if(not zone):
        return bad_request(f'Zone with id={id} does not exist')
    zone_schema = ZoneSchema()
    return jsonify(zone_schema.dump(zone))

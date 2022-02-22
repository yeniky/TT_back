from app.api import bp
from flasgger import swag_from
from app.schemas import AlertSchema
from app.swagger.alerts_specs import get_spec, post_spec, get_history_spec, get_zone_history_spec, get_tag_history_spec
from app.api.alerts.service import alert_list, close, alert_history, zone_alert_history, tag_alert_history
from app.api.errors import bad_request
from flask import jsonify, request
from app.models import Tag, Zone
from app.api.users.service import token_auth
from app.utils.helpers import build_page
import requests


@bp.route('/alerts', methods=['GET'])
@swag_from(get_spec)
def get_alerts():
    alerts = alert_list()
    alert_schema = AlertSchema(many=True)
    return jsonify(alert_schema.dump(alerts))


@bp.route('/alerts/<id>', methods=['POST'])
@swag_from(post_spec)
@token_auth.login_required
def close_alert(id):
    user = token_auth.current_user()
    alert = close(id, user)
    if(not alert):
        return bad_request(f'Alert with id={id} does not exist or already closed')
    alert_schema = AlertSchema()
    try:
        requests.post('http://127.0.0.1:5001/closed_alert',
                      json={'data': alert_schema.dump(alert)})
    except requests.exceptions.ConnectionError as ec:
        print("Connection Error:", ec)
        pass
    return jsonify(alert_schema.dump(alert))


@bp.route('/alerts/history', methods=['GET'])
@swag_from(get_history_spec)
def get_alert_history():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', "")
    order = request.args.get('order', "asc")

    alerts = alert_history(order_by, order).paginate(page, per_page, False)
    alert_schema = AlertSchema(many=True)
    return jsonify(build_page(alert_schema, alerts, order_by, order))


@bp.route('/alerts/zone_history/<id>', methods=['GET'])
@swag_from(get_zone_history_spec)
def get_zone_alert_history(id):

    zone = Zone.query.get(id)
    if(not zone):
        return bad_request(f'Zone with id={id} does not exist')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', "")
    order = request.args.get('order', "asc")

    alerts = zone_alert_history(
        id, order_by, order).paginate(page, per_page, False)
    alert_schema = AlertSchema(many=True)

    return jsonify(build_page(alert_schema, alerts, order_by, order, lambda a: a[0]))


@bp.route('/alerts/tag_history/<id>', methods=['GET'])
@swag_from(get_tag_history_spec)
def get_tag_alert_history(id):
    tag = Tag.query.get(id)
    if(not tag):
        return bad_request(f'Tag with id={id} does not exist')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', "")
    order = request.args.get('order', "asc")
    alerts = tag_alert_history(
        id, order_by, order).paginate(page, per_page, False)
    alert_schema = AlertSchema(many=True)

    return jsonify(build_page(alert_schema, alerts, order_by, order, lambda a: a[0]))

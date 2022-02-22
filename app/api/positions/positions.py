from flask import jsonify, request

from app.api import bp
from app.api.errors import bad_request
import requests
from app.api.positions.service import add_positions, get_alerts
from app.schemas import TagSchema, AlertSchema


@bp.route('/positions', methods=['POST'])
def create_positions():
    data = request.get_data().decode('utf-8').split('\n')
    if data is None:
        return bad_request('invalid post message')

    tags = [tag for tag in add_positions(data) if tag.active]
    alerts = get_alerts(tags)

    tag_schema = TagSchema(many=True)
    alert_schema = AlertSchema(many=True)

    if len(tags) > 0:
        try:
            requests.post('http://127.0.0.1:5001/data_message',
                          json={'data': tag_schema.dump(tags)})
        except requests.exceptions.ConnectionError as ec:
            print("Connection Error:", ec)
            pass

        try:
            if len(alerts):
                requests.post('http://127.0.0.1:5001/data_alert',
                              json={'data': alert_schema.dump(alerts)})
        except requests.exceptions.ConnectionError as ec:
            print("Connection Error:", ec)
            pass
        return jsonify({"status": "OK"})

    return bad_request("no data parsed")

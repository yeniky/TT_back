from flasgger import swag_from
from flask import request, jsonify
from app.models import Info
from app.api.errors import bad_request
from app.api import bp
from app.schemas import InfoSchema
from app.api.info.service import app_info
from app.swagger.info_specs import get_spec, put_spec
from app import db


@bp.route('/info', methods=['GET'])
@swag_from(get_spec)
def get_info():
    info = app_info()
    info_schema = InfoSchema()
    return jsonify(info_schema.dump(info))


@bp.route('/info', methods=['PUT'])
@swag_from(put_spec)
def edit_info():
    data = request.get_json()
    data['id'] = 1
    info_schema = InfoSchema()
    info = info_schema.load(
        data, session=db.session)
    db.session.add(info)
    db.session.commit()

    return jsonify(info_schema.dump(info))

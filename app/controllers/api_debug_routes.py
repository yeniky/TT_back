from app.models import Zone, Info, User
from flask import Blueprint
from app import db
import json
bp = Blueprint('api_debug_routes', __name__)


@bp.route('/first_time')
def setup():
    db.drop_all()
    db.create_all()
    init_admin()
    # init_zones()
    init_info()
    db.session.commit()
    return "DONE"


def init_zones():
    with open('app/controllers/zones.json') as f:
        zones = json.load(f)
        for zone in zones:
            min_x = zone['area'][0][0]
            min_y = zone['area'][0][1]
            max_x = zone['area'][1][0]
            max_y = zone['area'][1][1]
            new_zone = Zone(alias=zone['name'], min_x=min_x,
                            min_y=min_y, max_x=max_x, max_y=max_y)
            db.session.add(new_zone)


def init_admin():
    admin = User(username='admin', role='Admin')
    admin.set_password('password')
    db.session.add(admin)


def init_info():
    info = Info()
    db.session.add(info)

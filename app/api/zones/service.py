from app.models import Zone, ZoneEntry
from app import db
from app.utils.helpers import generate_order_by


def zone_list():
    return Zone.query.all()


def zone_history(id, order_by, order):
    result = ZoneEntry.query.filter_by(zone_id=id)
    if order_by:
        result = generate_order_by(result, ZoneEntry, order_by, order)
    return result


def deactivate(id):
    zone = Zone.query.get(id)
    if(zone):
        zone.active = False
        db.session.commit()
    return zone

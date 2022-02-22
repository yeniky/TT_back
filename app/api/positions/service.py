from app.models import Position, Tag, Zone, Alert
from app import db
from app.utils.helpers import Utils
from datetime import datetime


def add_positions(data):
    tags = []
    for message in data:
        new_position = create_pos(message)
        if type(new_position) == Tag:
            tags.append(new_position)
    db.session.commit()
    return tags


def create_pos(message):

    data = Utils.parse_message(message)
    if data == "invalid message":
        return
    tag = Tag.query.filter_by(address=data['addr']).first()
    # proteccion (activar para evitar DDoS a partir de mensajes)
    last_pos_time = Position.query.filter_by(
        tag=tag).order_by(Position.id.desc()).first()
    if tag:
        time_elapsed = datetime.utcnow() - last_pos_time.timestamp
        if time_elapsed.seconds < 1:
            return
    else:
        tag = Tag(address=data['addr'])
        db.session.add(tag)
        db.session.commit()

    zones = Zone.query.all()
    zone = Utils.check_zones([data['x'], data['y']], zones)
    position = Position.create(
        data['x'], data['y'], data['z'], data['signal'], tag, zone)
    return position.tag


def get_alerts(tags):
    result = []
    for t in tags:
        result.extend(Alert.query.filter_by(
            tag_id=t.id, timestamp=t.last_timestamp).all())
    return result

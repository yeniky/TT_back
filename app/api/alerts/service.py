from app.models import Alert, AlertRule
from datetime import datetime
from app import db
from app.utils.helpers import generate_order_by


def alert_list():
    return Alert.query.filter_by(active=True).all()


def close(id, user):
    alert = Alert.query.get(id)
    if(alert.active == False):
        return None
    if(alert):
        alert.active = False
        alert.close_timestamp = datetime.utcnow()
        alert.user_id = user.id
        db.session.commit()
    return alert


def alert_history(order_by, order):
    result = Alert.query
    if order_by:
        result = generate_order_by(result, Alert, order_by, order)
    return result


def zone_alert_history(id, order_by, order):

    result = db.session.query(Alert, AlertRule).filter(Alert.rule_id == AlertRule.id).filter(
        Alert.zone_id == id).filter(AlertRule.owner_type == 'zone_alert_rule')
    if order_by:
        result = generate_order_by(result, Alert, order_by, order)
    return result


def tag_alert_history(id, order_by, order):
    result = db.session.query(Alert, AlertRule).filter(Alert.rule_id == AlertRule.id).filter(
        Alert.tag_id == id).filter(AlertRule.owner_type == 'tag_alert_rule')
    if order_by:
        result = generate_order_by(result, Alert, order_by, order)
    return result

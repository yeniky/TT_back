from app import db
import enum
from datetime import datetime, timedelta
from sqlalchemy.orm import with_polymorphic, backref
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import os


class Role(enum.Enum):
    User = "User"
    Admin = "Admin"

    def __str__(self):
        return self.value


class Alert_type(enum.Enum):
    Entry = "Entry"
    Exit = "Exit"
    Permanence = "Permanence"


class Tag_type(enum.Enum):
    Person = "Person"
    Object = "Object"
    Vehicle = "Vehicle"

    def __str__(self):
        return self.value


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    alerts = db.relationship('Alert', backref='user')
    role = db.Column(db.Enum(Role), default=Role.User)
    active = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=36000):
        # now = datetime.utcnow()
        # if self.token and self.token_expiration > now + timedelta(seconds=60):
        #     return self.token
        if not self.token:
            self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        # self.token_expiration = now + timedelta(seconds=expires_in)
        # # db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        # if user is None or user.token_expiration < datetime.utcnow():
        #     return None
        if user is None:
            return None
        return user


class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(20), nullable=False, default='Client')
    place = db.Column(db.String(20), nullable=False, default='Place')


class TagConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(Tag_type), nullable=False)
    alias = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(50), default='')
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship("Tag", back_populates="config")
    alerts = db.relationship(
        'TagAlertRule', backref='tag_config', cascade='all, delete, delete-orphan')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    signal = db.Column(db.Integer)
    last_timestamp = db.Column(db.DateTime())
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))
    last_x = db.Column(db.Numeric(precision=18, scale=5))
    last_y = db.Column(db.Numeric(precision=18, scale=5))
    last_z = db.Column(db.Numeric(precision=18, scale=5))
    positions = db.relationship('Position', backref='tag')
    active = db.Column(db.Boolean, default=True)
    config = db.relationship(
        "TagConfig", uselist=False, back_populates="tag", cascade='all, delete, delete-orphan')
    # activated_alerts = db.relationship(
    #     'Alert', cascade='all, delete, delete-orphan')
    last_zone_timestamp = db.Column(db.DateTime())

    def update_position(self, position):
        self.last_x = position.x
        self.last_y = position.y
        self.last_z = position.z
        self.signal = position.signal

        alerts = []
        if(self.config and self.active):
            alerts = Alert.get_alerts(self, position)

        if(self.zone != position.zone or not self.last_zone_timestamp):
            if(self.last_zone_timestamp):
                Alert.create_in_out_alerts(alerts, self, position)
                ZoneEntry.change_old_zone_entry(
                    self, self.zone, position.timestamp)

            ZoneEntry.create_new_zone_entry(
                self, position.zone, position.timestamp)
            self.last_zone_timestamp = position.timestamp

        Alert.create_permanence_alerts(alerts, self, position)

        self.zone = position.zone
        self.last_timestamp = position.timestamp
        db.session.commit()
        return self


class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(20), default='no zone', unique=True)
    description = db.Column(db.String(50), default='')
    min_x = db.Column(db.Numeric(precision=18, scale=5))
    min_y = db.Column(db.Numeric(precision=18, scale=5))
    max_x = db.Column(db.Numeric(precision=18, scale=5))
    max_y = db.Column(db.Numeric(precision=18, scale=5))
    tags = db.relationship('Tag', backref='zone')
    active = db.Column(db.Boolean, default=True)
    positions = db.relationship('Position', backref='zone')
    alerts = db.relationship(
        'ZoneAlertRule', backref='zone', cascade='all, delete, delete-orphan')
    tag_alerts = db.relationship('TagAlertRule', backref='zone')


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    signal = db.Column(db.Integer)
    x = db.Column(db.Numeric(precision=18, scale=5))
    y = db.Column(db.Numeric(precision=18, scale=5))
    z = db.Column(db.Numeric(precision=18, scale=5))
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    @ staticmethod
    def create(x, y, z, signal, tag, zone):
        if(zone and not zone.active):
            zone = None
        new_pos = Position(x=x, y=y, z=z, signal=signal,
                           zone=zone, timestamp=datetime.utcnow())
        tag.update_position(new_pos)
        new_pos.tag = tag
        db.session.add(new_pos)
        db.session.commit()
        return new_pos


class AlertRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.Enum(Alert_type), nullable=False)
    time = db.Column(db.Integer, nullable=True)
    owner_type = db.Column(db.String(20))
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))
    active = db.Column(db.Boolean, default=True)

    __mapper_args__ = {
        'polymorphic_on': owner_type,
        'polymorphic_identity': 'alert_rule',
    }


class TagAlertRule(AlertRule):
    tag_config_id = db.Column(db.Integer, db.ForeignKey('tag_config.id'))
    __mapper_args__ = {
        'polymorphic_identity': 'tag_alert_rule'
    }


class ZoneAlertRule(AlertRule):
    tag_type = db.Column(db.Enum(Tag_type))

    __mapper_args__ = {
        'polymorphic_identity': 'zone_alert_rule'
    }


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)
    close_timestamp = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))
    zone = db.relationship('Zone', uselist=False,
                           backref=backref("alert", cascade="all,delete"))

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship('Tag', uselist=False,
                          backref=backref("alert", cascade="all,delete"))

    rule_id = db.Column(db.Integer, db.ForeignKey('alert_rule.id'))
    rule = db.relationship('AlertRule', uselist=False,
                           backref=backref("alert", cascade="all,delete"))

    @ staticmethod
    def get_alerts(tag, position):
        tag_alerts = db.session.query(AlertRule).with_polymorphic([TagAlertRule]).filter(AlertRule.active == True).filter(
            TagAlertRule.tag_config == tag.config, (TagAlertRule.zone == tag.zone) | (TagAlertRule.zone == position.zone)).all()
        zone_alerts = db.session.query(AlertRule).with_polymorphic([ZoneAlertRule]).filter(AlertRule.active == True).filter(ZoneAlertRule.tag_type == tag.config.type,
                                                                                                                            (ZoneAlertRule.zone == tag.zone) | (ZoneAlertRule.zone == position.zone)).all()
        return tag_alerts+zone_alerts

    @ staticmethod
    def create_permanence_alerts(alerts, tag, position):
        for a in alerts:
            Alert.check_permanence_alert(a, tag, position)

    @ staticmethod
    def create_in_out_alerts(alerts, tag, position):
        for a in alerts:
            Alert.check_in_out_alert(a, tag, position)

    @ staticmethod
    def check_in_out_alert(*args):
        Alert.check_entry_alert(*args)
        Alert.check_exit_alert(*args)
        db.session.commit()

    @ staticmethod
    def check_entry_alert(rule, tag, position):
        if(position.zone == rule.zone and rule.zone.active and rule.alert_type == Alert_type.Entry and Alert.check_unique(rule, tag)):
            new_alert = Alert(timestamp=position.timestamp,
                              zone_id=rule.zone_id, rule_id=rule.id, tag_id=tag.id)
            db.session.add(new_alert)

    @ staticmethod
    def check_exit_alert(rule, tag, position):
        if(tag.zone == rule.zone and rule.zone.active and rule.alert_type == Alert_type.Exit and Alert.check_unique(rule, tag)):
            new_alert = Alert(timestamp=position.timestamp,
                              zone_id=rule.zone_id, rule_id=rule.id, tag_id=tag.id)
            db.session.add(new_alert)

    @ staticmethod
    def check_permanence_alert(rule, tag, position):
        if(tag.zone == rule.zone and position.zone == rule.zone and rule.zone.active and rule.alert_type == Alert_type.Permanence and Alert.check_unique(rule, tag)):
            permanence = (position.timestamp -
                          tag.last_zone_timestamp).seconds/60 >= rule.time
            if(permanence):
                new_alert = Alert(timestamp=position.timestamp,
                                  zone_id=rule.zone_id, rule_id=rule.id, tag_id=tag.id)
                db.session.add(new_alert)

    @ staticmethod
    def check_unique(rule, tag):
        return Alert.query.filter_by(tag_id=tag.id, active=True, rule_id=rule.id).count() == 0


class ZoneEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))
    zone = db.relationship('Zone', uselist=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship('Tag', uselist=False)
    in_timestamp = db.Column(db.DateTime)
    out_timestamp = db.Column(db.DateTime, nullable=True)
    permanence_time = db.Column(db.Numeric)

    @ staticmethod
    def change_old_zone_entry(tag, zone, date):
        old_entry = ZoneEntry.query.filter_by(
            tag_id=tag.id, zone=zone, out_timestamp=None).first()
        if(old_entry):
            old_entry.out_timestamp = date
            old_entry.permanence_time = (
                old_entry.out_timestamp - old_entry.in_timestamp).seconds/60
            db.session.commit()

    @ staticmethod
    def create_new_zone_entry(tag, zone, date):
        new_entry = ZoneEntry(tag_id=tag.id,
                              zone=zone, in_timestamp=date)
        db.session.add(new_entry)
        db.session.commit()

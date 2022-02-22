from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Tag, Zone, Position, TagConfig, Tag_type, Alert_type, AlertRule
from app.models import TagAlertRule, ZoneAlertRule, Alert, ZoneEntry, User, Role, Info
from marshmallow_sqlalchemy.fields import Nested, fields
from marshmallow_enum import EnumField
from marshmallow import validate, post_dump, pre_load, post_load, pre_dump
from marshmallow import ValidationError, validates_schema, Schema
from werkzeug.security import generate_password_hash


class UserSchema(SQLAlchemyAutoSchema):

    email = fields.Str(required=True)
    password = fields.Str()
    role = EnumField(Role, by_value=True)

    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        dump_only = ('role', 'active')
        exclude = ("token", "token_expiration",
                   "password_hash", "alerts")

    @validates_schema
    def validate_email(self, data, **kwargs):
        if('email' in data):
            user = User.query.filter_by(email=data['email']).first()
            if (not('id' in data) and user):
                raise ValidationError(
                    'A user with that email already exists', field_name='email')

            if (('id' in data) and user and user.id != data['id']):
                raise ValidationError(
                    'A user with that email already exists', field_name='email')


class InfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Info
        load_instance = True
        load_only = ('id',)


class PositionSchema(SQLAlchemyAutoSchema):
    x = fields.Float()
    y = fields.Float()

    class Meta:
        model = Position
        include_relationships = True
        load_instance = True
        exclude = ('z', 'signal', 'zone', 'id', 'tag')


class AlertRuleSchema(Schema):

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if value is not None
        }

    @validates_schema
    def validate_time(self, data, **kwargs):
        if ('time' in data and data['alert_type'] != Alert_type.Permanence) or ((not ('time' in data)) and data['alert_type'] == Alert_type.Permanence):
            raise ValidationError(
                'Only Permanence alert type can have time parameter')
        if ('time' in data and data['time'] < 1):
            raise ValidationError('Time must be greater than 0')


class ZoneAlertRuleSchema(SQLAlchemyAutoSchema, AlertRuleSchema):
    tag_type = EnumField(Tag_type, by_value=True, required=True)
    alert_type = EnumField(Alert_type, by_value=True, required=True)

    class Meta:
        model = ZoneAlertRule
        include_relationships = True
        load_instance = True
        exclude = ('owner_type', 'alert')


class ZoneSchema(SQLAlchemyAutoSchema):

    area = fields.List(fields.List(fields.Float()))

    class Meta:
        model = Zone
        include_relationships = True
        load_instance = True
        exclude = ("tags", "tag_alerts", "positions",
                   "min_x", "min_y", "max_x", "max_y", "alert")

    # def create_area(self, obj):
    #     return [[obj.min_x, obj.min_y], [obj.max_x, obj.max_y]]

    # def load_area(self, value):
    #     return list(value)

    alerts = Nested(ZoneAlertRuleSchema, many=True,
                    exclude=('zone',))

    @pre_dump
    def set_area(self, data, **kwargs):
        data.area = [[data.min_x, data.min_y], [data.max_x, data.max_y]]
        return data

    @post_load
    def get_area(self, data, **kwargs):
        print(data)
        if('area' in data):
            data['min_x'] = data['area'][0][0]
            data['min_y'] = data['area'][0][1]
            data['max_x'] = data['area'][1][0]
            data['max_y'] = data['area'][1][1]
            del data['area']
        return data

    @validates_schema
    def validate_name(self, data, **kwargs):
        if('alias' in data):
            zone = Zone.query.filter_by(alias=data['alias']).first()
            if (not('id' in data) and zone):
                raise ValidationError(
                    'A zone with that alias already exists', field_name='alias')
            if (('id' in data) and zone and zone.id != data['id']):
                raise ValidationError(
                    'A zone with that alias already exists', field_name='alias')


class TagAlertRuleSchema(SQLAlchemyAutoSchema, AlertRuleSchema):
    alert_type = EnumField(Alert_type, by_value=True, required=True)

    class Meta:
        model = TagAlertRule
        include_relationships = True
        load_instance = True
        exclude = ('owner_type', 'alert')
    zone = Nested(ZoneSchema, many=False, only=("alias", "id"))


class TagConfigSchema(SQLAlchemyAutoSchema):
    type = EnumField(Tag_type, by_value=True, required=True)
    description = fields.Str(required=True, validate=[validate.Length(max=50)])
    alias = fields.Str(required=True, validate=[validate.Length(max=20)])

    class Meta:
        model = TagConfig
        include_relationships = True
        load_instance = True
        exclude = ('tag',)
        load_only = ('id',)

    alerts = Nested(TagAlertRuleSchema, many=True,
                    exclude=('tag_config',))

    @validates_schema
    def validate_name(self, data, **kwargs):
        if('alias' in data):
            config = TagConfig.query.filter_by(alias=data['alias']).first()
            if (not('id' in data) and config):
                raise ValidationError(
                    'A tag with that alias already exists', field_name='alias')
            if (('id' in data) and config and config.id != data['id']):
                raise ValidationError(
                    'A tag with that alias already exists', field_name='alias')


class TagSchema(SQLAlchemyAutoSchema):
    last_x = fields.Float()
    last_y = fields.Float()
    last_z = fields.Float()

    class Meta:
        model = Tag
        include_relationships = True
        load_instance = True
        exclude = ("positions", "last_zone_timestamp", "alert")

    zone = Nested(ZoneSchema, many=False, only=("alias", "id"))
    config = Nested(TagConfigSchema, many=False, exclude=("tag", "id"))


class AlertSchema(SQLAlchemyAutoSchema):
    alert_type = fields.Method('get_alert_type')
    owner_type = fields.Method('get_owner_type')
    time = fields.Method('get_time')

    class Meta:
        model = Alert
        include_relationships = True
        load_instance = True
        exclude = ('rule',)

    def get_alert_type(self, obj):
        return obj.rule.alert_type.value

    def get_owner_type(self, obj):
        return obj.rule.owner_type

    def get_time(self, obj):
        if(obj.rule.alert_type == Alert_type.Permanence):
            return obj.rule.time
        return None

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if (value is not None) or (value is None and key != 'time')
        }
    zone = Nested(ZoneSchema, many=False, only=("alias", "id"))
    tag = Nested(TagSchema, many=False, only=(
        "address", "id", "config"), exclude=('config.alerts', 'config.description'))
    user = Nested(UserSchema, many=False, only=("username", "id"))


class ZoneEntrySchema(SQLAlchemyAutoSchema):
    permanence_time = fields.Float()

    class Meta:
        model = ZoneEntry
        include_relationships = True
        load_instance = True
        exclude = ('id',)

    zone = Nested(ZoneSchema, many=False, only=("alias", "id"))
    tag = Nested(TagSchema, many=False, only=(
        "address", "id", "config"), exclude=('config.alerts', 'config.description'))


class PasswordSchema(Schema):
    password = fields.Str(required=True)
    old_password = fields.Str(required=True)

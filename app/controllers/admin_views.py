from app import admin, db
from flask_admin.contrib.sqla import ModelView
from app.models import Tag, Position, Zone, TagConfig, ZoneEntry
from app.models import TagAlertRule, ZoneAlertRule, AlertRule, Alert, User, Info


admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Position, db.session))
admin.add_view(ModelView(Zone, db.session))
admin.add_view(ModelView(TagConfig, db.session))
admin.add_view(ModelView(AlertRule, db.session))
admin.add_view(ModelView(ZoneAlertRule, db.session))
admin.add_view(ModelView(TagAlertRule, db.session))
admin.add_view(ModelView(Alert, db.session))
admin.add_view(ModelView(ZoneEntry, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Info, db.session))

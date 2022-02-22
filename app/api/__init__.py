
from flask import Blueprint
bp = Blueprint('api', __name__)
from app.api.tags import tags
from app.api.zones import zones
from app.api.positions import positions
from app.api.alerts import alerts
from app.api.utility import utility
from app.api.users import users
from app.api.info import info

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_admin import Admin
from config import Config
from flasgger import Swagger
from flask_marshmallow import Marshmallow
from apispec.ext.marshmallow import MarshmallowPlugin
from app.utils.marshmellow_plugin import enum_to_properties
from apispec import APISpec
import flask_excel as excel
from flask_mail import Mail

db = SQLAlchemy()
admin = Admin(name="Bayer Admin")
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../client/build/',
                instance_relative_config=True)
    app.config.from_object(config_class)
    # DB
    db.init_app(app)

    # Mail
    app.config['MAIL_SERVER'] = 'smtp.office365.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'tranckandtrace@outlook.com'
    app.config['MAIL_PASSWORD'] = 'lqnrchjzofokckyb'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail.init_app(app)

    # Marshmallow
    Marshmallow(app)
    marshmallow_plugin = MarshmallowPlugin()
    app.config.update({
        'APISPEC_SPEC': APISpec(title="AAAAA", version="0.1", openapi_version="3.0.0", plugins=(marshmallow_plugin,)),
        'APISPEC_SWAGGER_URL': '/swagger/',
    })
    marshmallow_plugin.converter.add_attribute_function(enum_to_properties)

    # Swagger
    Swagger(app)

    # Excel
    excel.init_excel(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    admin.init_app(app)
    import app.controllers.admin_views as admin_routes

    from app.api import bp as api_routes
    app.register_blueprint(api_routes, url_prefix='/api')

    from app.controllers.api_debug_routes import bp as debug_routes
    app.register_blueprint(debug_routes, url_prefix='/debug')

    from app import models
    return app

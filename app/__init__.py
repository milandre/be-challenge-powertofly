from flask import Flask
from flask_caching import Cache
from flask_migrate import Migrate
from flask_resty import Api

from config import config

from .api import views
from .api.models import db
from .api.schemas import UserSchema


def create_app(config_name):
    # Configure flask app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # ReDoc config
    app.config['REDOC'] = {'marshmallow_schemas': [UserSchema]}

    # Init and migrate database
    db.init_app(app)
    Migrate(app, db)

    # Create app blueprints
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Create api routes
    api = Api(app, prefix='/api')
    api.add_resource("/users/", views.UserListView)

    # Init cache
    views.cache.init_app(app)

    return app


def create_cache(app):
    return Cache(app)

# /auth-service/app/__init__.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .util.exceptions import ServiceError

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(ServiceError)
    def handle_service_error(error):
        response = jsonify({'error': str(error)})
        response.status_code = error.status_code
        return response

    from . import models
    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
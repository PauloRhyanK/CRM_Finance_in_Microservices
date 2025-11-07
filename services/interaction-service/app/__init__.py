# /interaction-service/app/__init__.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .util.exceptions import ServiceError

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    @app.errorhandler(ServiceError)
    def handle_service_error(error):
        response = jsonify({'error': str(error)})
        response.status_code = error.status_code
        return response

    with app.app_context():
        from . import models    
    from .routes import interaction_bp
    app.register_blueprint(interaction_bp)

    return app
from flask import Flask
from routes import register_routes

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('config.Config')

    # Register routes
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
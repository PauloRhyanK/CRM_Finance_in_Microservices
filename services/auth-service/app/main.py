from flask import Flask
from routes import auth_routes

app = Flask(__name__)

# Register the authentication routes
app.register_blueprint(auth_routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
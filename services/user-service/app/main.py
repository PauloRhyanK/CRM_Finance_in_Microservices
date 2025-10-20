from flask import Flask
from routes import user_routes

app = Flask(__name__)

# Register the user routes
app.register_blueprint(user_routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
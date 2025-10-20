from flask import Flask
from routes import order_routes

app = Flask(__name__)

# Register the order routes
app.register_blueprint(order_routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
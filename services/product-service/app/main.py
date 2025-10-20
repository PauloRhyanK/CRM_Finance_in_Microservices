from flask import Flask
from routes import product_routes

app = Flask(__name__)

# Register the product routes
app.register_blueprint(product_routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
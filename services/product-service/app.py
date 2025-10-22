# /product-service/app.py
import os
from app import create_app
from config import config_by_name

config_name = os.getenv('FLASK_ENV', 'default')
config_object = config_by_name[config_name]
app = create_app(config_object)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
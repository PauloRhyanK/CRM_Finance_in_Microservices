# /services/auth-service/manage.py (CORRIGIDO)

import os
from app import create_app, db
from config import config_by_name
from flask_migrate import Migrate

# IMPORTANTE: Importe os seus modelos aqui!
from app import models 

config_name = os.getenv('FLASK_ENV', 'default')
config_object = config_by_name[config_name]
app = create_app(config_object)
migrate = Migrate(app, db)
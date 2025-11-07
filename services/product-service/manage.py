# /services/auth-service/manage.py (VERSÃO CORRETA PARA CLI)
import os
from app import create_app, db
from config import config_by_name
from flask_migrate import Migrate

# Importar os modelos é crucial para o 'migrate' os encontrar
from app import models 

config_name = os.getenv('FLASK_ENV', 'default')
config_object = config_by_name[config_name]

app = create_app(config_object)
migrate = Migrate(app, db)

# Isto permite que o Flask CLI encontre a 'app'
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Product=models.Product) # Adicione seus modelos aqui
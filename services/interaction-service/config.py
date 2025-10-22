# /interaction-service/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    
    # URL de conexão específica para este serviço
    SQLALCHEMY_DATABASE_URI = os.environ.get('INTERACTION_DATABASE_URL')

    # URLs dos serviços dos quais dependemos
    # Estes valores virão do docker-compose
    CUSTOMER_SERVICE_URL = os.environ.get('CUSTOMER_SERVICE_URL')
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
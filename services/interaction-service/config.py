# /interaction-service/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('INTERACTION_DATABASE_URL')

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
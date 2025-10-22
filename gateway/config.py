# /gateway/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') # Necessário para Flask
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    JSON_AS_ASCII = False
    
    # Chave para verificar os tokens JWT (deve ser a MESMA usada no auth-service)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') 
    
    # URLs dos microserviços
    AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL')
    CUSTOMER_SERVICE_URL = os.environ.get('CUSTOMER_SERVICE_URL')
    PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL')
    INTERACTION_SERVICE_URL = os.environ.get('INTERACTION_SERVICE_URL')
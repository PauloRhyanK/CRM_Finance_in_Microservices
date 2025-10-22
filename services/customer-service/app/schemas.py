# /customer-service/app/schemas.py
from . import ma
from .models import Customer
from marshmallow import fields

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = False # Não há chaves estrangeiras para incluir
        
    ds_customer_email = fields.Email(required=True)
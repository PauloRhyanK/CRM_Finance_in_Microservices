# /interaction-service/app/schemas.py
from . import ma
from .models import Interaction, Transaction
from marshmallow import fields, validate

class InteractionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Interaction
        load_instance = True
    
    cd_customer = fields.UUID(required=True)
    cd_user = fields.UUID(required=True)
    ds_notes = fields.Str(required=True, validate=validate.Length(min=5))
    id_interaction_type = fields.Str(
        required=True, 
        validate=validate.OneOf(['venda', 'ligacao', 'email', 'reuniao', 'contato'])
    )

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        load_instance = True
    
    cd_customer = fields.UUID(required=True)
    cd_user = fields.UUID(required=True)
    vr_transaction = fields.Decimal(required=True, places=2)
    id_transaction_type = fields.Int(required=True, validate=validate.OneOf([1, 2]))
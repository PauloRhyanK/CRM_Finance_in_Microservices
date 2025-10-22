# /product-service/app/schemas.py
from . import ma
from .models import Product
from marshmallow import fields, validate

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = False

    ds_product_name = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    vr_price = fields.Decimal(required=True, places=2, validate=validate.Range(min=0))
    id_product_type = fields.Str(required=True, validate=validate.OneOf(['produto', 'servico']))
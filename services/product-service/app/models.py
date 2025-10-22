# /product-service/app/models.py
import enum
from . import db
from sqlalchemy import Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class ProductType(enum.Enum):
    PRODUTO = 'produto'
    SERVICO = 'servico'

class Product(db.Model):
    __tablename__ = 'product'
    
    cd_product = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ds_product_name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    ds_product_description = db.Column(db.Text, nullable=True)
    
    vr_price = db.Column(Numeric(10, 2), CheckConstraint('vr_price >= 0'), nullable=False)
    
    # A correção para o Enum funcionar com PostgreSQL
    id_product_type = db.Column(
        db.Enum(ProductType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=ProductType.PRODUTO
    )
    
    dt_created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dt_updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'<Product {self.ds_product_name}>'
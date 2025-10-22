# /customer-service/app/models.py
from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customer'
    
    cd_customer = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ds_customer_name = db.Column(db.String(255), nullable=False)
    ds_customer_email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    ds_customer_phone = db.Column(db.String(20), nullable=True)
    ds_customer_cpf_cnpj = db.Column(db.String(18), unique=True, nullable=True)
    
    ds_customer_address = db.Column(db.String(500), nullable=True)
    ds_customer_city = db.Column(db.String(100), nullable=True)
    ds_customer_state = db.Column(db.String(2), nullable=True)
    ds_customer_zip_code = db.Column(db.String(10), nullable=True)
    ds_customer_country = db.Column(db.String(100), nullable=True, default='Brasil')
    
    dt_customer_created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dt_customer_updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_customer_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relação com transações foi REMOVIDA.
    # Este serviço não precisa de saber sobre transações.
    
    def validate_cpf_cnpj(self):
        if not self.ds_customer_cpf_cnpj:
            return True
        cpf_cnpj = ''.join(filter(str.isdigit, self.ds_customer_cpf_cnpj))
        return len(cpf_cnpj) in [11, 14]

    def __repr__(self):
        return f'<Customer {self.ds_customer_email}>'
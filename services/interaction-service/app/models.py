# /interaction-service/app/models.py
import enum
from . import db
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

# --- Modelo de Interação ---
class InteractionType(enum.Enum):
    VENDA = 'venda'
    LIGACAO = 'ligacao'
    EMAIL = 'email'
    REUNIAO = 'reuniao'
    CONTATO = 'contato'

class Interaction(db.Model):
    __tablename__ = 'interaction'
    cd_interaction = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ds_notes = db.Column(db.Text, nullable=False)
    id_interaction_type = db.Column(
        db.Enum(InteractionType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=InteractionType.CONTATO
    )
    dt_interaction = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dt_created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dt_updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Chaves "estrangeiras" para outros serviços
    cd_customer = db.Column(UUID(as_uuid=True), nullable=False, index=True)
    cd_user = db.Column(UUID(as_uuid=True), nullable=False, index=True)

# --- Modelo de Transação ---
class TransactionType(enum.Enum):
    ENTRADA = 1
    SAIDA = 2

class Transaction(db.Model):
    __tablename__ = 'transaction'
    cd_transaction = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vr_transaction = db.Column(Numeric(10, 2), nullable=False)
    id_transaction_type = db.Column(
        db.Enum(TransactionType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    dt_transaction = db.Column(db.Date, nullable=False)
    dt_transaction_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Chaves "estrangeiras" para outros serviços
    cd_customer = db.Column(UUID(as_uuid=True), nullable=False, index=True)
    cd_user = db.Column(UUID(as_uuid=True), nullable=False, index=True)
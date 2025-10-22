from enum import Enum as PyEnum
from datetime import datetime
from . import db

class InteractionType(PyEnum):
    EMAIL = 'email'
    CALL = 'call'
    MEETING = 'meeting'
    NOTE = 'note'

class TransactionType(PyEnum):
    SALE = 'sale'
    REFUND = 'refund'
    PAYMENT = 'payment'
    CREDIT = 'credit'

class Interaction(db.Model):
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False)
    interaction_type = db.Column(db.Enum(InteractionType), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    interaction_date = db.Column(db.DateTime, default=datetime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)

    def __repr__(self):
        return f'<Interaction {self.id} - {self.interaction_type.value}>'

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False, index=True)
    product_id = db.Column(db.Integer, nullable=True)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))
    transaction_date = db.Column(db.DateTime, default=datetime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)

    def __repr__(self):
        return f'<Transaction {self.id} - {self.transaction_type.value} - ${self.amount}>'
# /customer-service/app/services.py
from . import db
from .models import Customer
from .schemas import CustomerSchema
from .util.exceptions import CustomerNotFoundError, InvalidDataError
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from datetime import datetime

customer_schema = CustomerSchema()

def create_customer(customer_data):
    try:
        customer = customer_schema.load(customer_data, session=db.session)
        if not customer.validate_cpf_cnpj():
            raise InvalidDataError("CPF/CNPJ em formato inválido")
        db.session.add(customer)
        db.session.commit()
        return customer
    except ValidationError as err:
        raise InvalidDataError(err.messages)
    except IntegrityError:
        db.session.rollback()
        raise InvalidDataError("Email ou CPF/CNPJ já está em uso.")

def get_customer_by_id(customer_id):
    customer = Customer.query.filter_by(cd_customer=customer_id).first()
    if not customer:
        raise CustomerNotFoundError()
    return customer

def update_customer(customer_id, customer_data):
    customer = get_customer_by_id(customer_id) # Reutiliza a função de busca
    try:
        updated_customer = customer_schema.load(
            customer_data, instance=customer, partial=True, session=db.session
        )
        if 'ds_customer_cpf_cnpj' in customer_data and not updated_customer.validate_cpf_cnpj():
            raise InvalidDataError("CPF/CNPJ em formato inválido")
        db.session.commit()
        return updated_customer
    except ValidationError as err:
        raise InvalidDataError(err.messages)
    except IntegrityError:
        db.session.rollback()
        raise InvalidDataError("Email ou CPF/CNPJ já está em uso por outro cliente.")

def delete_customer(customer_id, soft_delete=True):
    customer = get_customer_by_id(customer_id)
    if soft_delete:
        customer.is_customer_active = False
    else:
        db.session.delete(customer)
    db.session.commit()
    return True

def activate_customer(customer_id):
    customer = get_customer_by_id(customer_id)
    customer.is_customer_active = True
    db.session.commit()
    return customer

def get_customers_list(args):
    page = args.get('page', 1)
    per_page = args.get('per_page', 20)
    active_only = args.get('active_only', True)
    search_term = args.get('search_term')
    query = Customer.query
    if active_only:
        query = query.filter(Customer.is_customer_active == True)
    if search_term:
        search_filter = f"%{search_term}%"
        conditions = [
            Customer.ds_customer_name.ilike(search_filter),
            Customer.ds_customer_email.ilike(search_filter),
            Customer.ds_customer_cpf_cnpj.ilike(search_filter)
        ]
        query = query.filter(or_(*conditions))
    paginated = query.order_by(Customer.ds_customer_name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return paginated
# /product-service/app/services.py
from . import db
from .models import Product
from .schemas import ProductSchema
from .util.exceptions import ProductNotFoundError, InvalidDataError
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

product_schema = ProductSchema()

def create_product(product_data):
    try:
        product = product_schema.load(product_data, session=db.session)
        db.session.add(product)
        db.session.commit()
        return product
    except ValidationError as err:
        raise InvalidDataError(err.messages)
    except IntegrityError:
        db.session.rollback()
        raise InvalidDataError("Um produto com este nome já existe.")

def get_product_by_id(product_id):
    product = Product.query.filter_by(cd_product=product_id).first()
    if not product:
        raise ProductNotFoundError()
    return product

def update_product(product_id, product_data):
    product = get_product_by_id(product_id)
    try:
        updated_product = product_schema.load(
            product_data, instance=product, partial=True, session=db.session
        )
        db.session.commit()
        return updated_product
    except ValidationError as err:
        raise InvalidDataError(err.messages)
    except IntegrityError:
        db.session.rollback()
        raise InvalidDataError("Um produto com este nome já existe.")

def delete_product(product_id, soft_delete=True):
    product = get_product_by_id(product_id)
    if soft_delete:
        product.is_active = False
    else:
        db.session.delete(product)
    db.session.commit()
    return True

def get_all_products(page=1, per_page=20, active_only=True):
    query = Product.query
    if active_only:
        query = query.filter(Product.is_active == True)
    paginated = query.order_by(Product.ds_product_name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return paginated
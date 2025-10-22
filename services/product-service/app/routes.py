# /product-service/app/routes.py
from flask import Blueprint, request, jsonify
from . import services
from .schemas import ProductSchema
# Você pode adicionar o decorador validate_uuid aqui se quiser

product_bp = Blueprint('product_api', __name__, url_prefix='/api/products')
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@product_bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data: return jsonify({'error': 'Dados não fornecidos'}), 400
    new_product = services.create_product(data)
    return jsonify({
        'message': 'Produto criado com sucesso',
        'product': product_schema.dump(new_product)
    }), 201

@product_bp.route('', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    paginated = services.get_all_products(page=page, per_page=per_page)
    return jsonify({
        'products': products_schema.dump(paginated.items),
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': paginated.page
    }), 200

@product_bp.route('/<string:product_id>', methods=['GET'])
def get_product(product_id):
    product = services.get_product_by_id(product_id)
    return jsonify({'product': product_schema.dump(product)}), 200

@product_bp.route('/<string:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    if not data: return jsonify({'error': 'Dados não fornecidos'}), 400
    updated = services.update_product(product_id, data)
    return jsonify({
        'message': 'Produto atualizado com sucesso',
        'product': product_schema.dump(updated)
    }), 200

@product_bp.route('/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    hard_delete = request.args.get('hard_delete', 'false').lower() == 'true'
    services.delete_product(product_id, soft_delete=not hard_delete)
    message = "Produto removido permanentemente" if hard_delete else "Produto desativado com sucesso"
    return jsonify({'message': message}), 200
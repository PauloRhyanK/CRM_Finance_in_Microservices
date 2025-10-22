# /customer-service/app/routes.py
from flask import Blueprint, request, jsonify
from . import services
from .schemas import CustomerSchema
from .util.decorators import validate_uuid

customer_bp = Blueprint('customer_api', __name__, url_prefix='/api/customers')
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@customer_bp.route('', methods=['POST'])
def create_customer():
    data = request.get_json()
    if not data: return jsonify({'error': 'Dados não fornecidos'}), 400
    new_customer = services.create_customer(data)
    return jsonify({
        'message': 'Cliente criado com sucesso',
        'customer': customer_schema.dump(new_customer)
    }), 201

@customer_bp.route('', methods=['GET'])
def get_customers():
    args = {
        'page': request.args.get('page', 1, type=int),
        'per_page': min(request.args.get('per_page', 20, type=int), 100),
        'active_only': request.args.get('active_only', 'true').lower() == 'true',
        'search_term': request.args.get('search')
    }
    paginated = services.get_customers_list(args)
    return jsonify({
        'customers': customers_schema.dump(paginated.items),
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': paginated.page
    }), 200

@customer_bp.route('/<string:customer_id>', methods=['GET'])
@validate_uuid('customer_id')
def get_customer(customer_id):
    customer = services.get_customer_by_id(customer_id)
    return jsonify({'customer': customer_schema.dump(customer)}), 200

@customer_bp.route('/<string:customer_id>', methods=['PUT'])
@validate_uuid('customer_id')
def update_customer(customer_id):
    data = request.get_json()
    if not data: return jsonify({'error': 'Dados não fornecidos'}), 400
    updated = services.update_customer(customer_id, data)
    return jsonify({
        'message': 'Cliente atualizado com sucesso',
        'customer': customer_schema.dump(updated)
    }), 200

@customer_bp.route('/<string:customer_id>', methods=['DELETE'])
@validate_uuid('customer_id')
def delete_customer(customer_id):
    hard_delete = request.args.get('hard_delete', 'false').lower() == 'true'
    services.delete_customer(customer_id, soft_delete=not hard_delete)
    message = "Cliente removido permanentemente" if hard_delete else "Cliente desativado com sucesso"
    return jsonify({'message': message}), 200

@customer_bp.route('/<string:customer_id>/activate', methods=['PATCH'])
@validate_uuid('customer_id')
def activate_customer(customer_id):
    activated = services.activate_customer(customer_id)
    return jsonify({
        'message': 'Cliente reativado com sucesso',
        'customer': customer_schema.dump(activated)
    }), 200
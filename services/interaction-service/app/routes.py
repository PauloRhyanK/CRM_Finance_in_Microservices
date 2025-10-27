# /interaction-service/app/routes.py
from flask import Blueprint, request, jsonify
from . import services
from .schemas import InteractionSchema

interaction_bp = Blueprint('interaction_api', __name__, url_prefix='/api/customers')
interaction_schema = InteractionSchema()
interactions_schema = InteractionSchema(many=True)

@interaction_bp.route('/<string:customer_id>/interactions', methods=['POST'])
def create_interaction(customer_id):
    """Cria um novo registro de interação para um cliente."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    user_id = request.headers.get('X-User-Id')
    if not user_id:
        return jsonify({'error': 'Não autorizado (ID de usuário ausente)'}), 401
    
    new_interaction = services.create_interaction(data, customer_id, user_id)
    
    return jsonify({
        'message': 'Interação registrada com sucesso',
        'interaction': interaction_schema.dump(new_interaction)
    }), 201

@interaction_bp.route('/<string:customer_id>/interactions', methods=['GET'])
def get_interactions(customer_id):
    """Lista todas as interações de um cliente."""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 15, type=int), 100)
    
    paginated = services.get_interactions_for_customer(
        customer_id, page=page, per_page=per_page
    )
    
    return jsonify({
        'interactions': interactions_schema.dump(paginated.items),
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': paginated.page
    }), 200


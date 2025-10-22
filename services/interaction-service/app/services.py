# /interaction-service/app/services.py
from . import db
from .models import Interaction
from .schemas import InteractionSchema, TransactionSchema
from .util.exceptions import InvalidDataError, CustomerNotFoundError
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import current_app
import requests

interaction_schema = InteractionSchema()
interactions_schema = InteractionSchema(many=True)

# --- LÓGICA DE VALIDAÇÃO (COMUNICAÇÃO ENTRE SERVIÇOS) ---

def _validate_customer_exists(customer_id):
    """
    Função interna para "perguntar" ao Serviço de Clientes se um cliente existe.
    Este é o coração da comunicação entre microserviços.
    """
    service_url = current_app.config['CUSTOMER_SERVICE_URL']
    try:
        response = requests.get(f"{service_url}/api/customers/{customer_id}")
        
        if response.status_code == 200:
            return True # Cliente existe
        elif response.status_code == 404:
            raise CustomerNotFoundError()
        else:
            # Outro erro (ex: serviço de cliente fora do ar)
            raise InvalidDataError(f"Erro ao validar cliente: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        # Erro de rede (não conseguiu se conectar ao serviço)
        raise ServiceError(f"Não foi possível conectar ao serviço de clientes: {e}", 503)

# --- LÓGICA DE INTERAÇÃO ---

def create_interaction(data, customer_id, user_id):
    """Cria um novo registro de interação."""
    
    # 1. Validar o ID do cliente chamando o outro serviço
    _validate_customer_exists(customer_id)
    
    try:
        # 2. Preparar os dados (combinando IDs e o JSON)
        data_to_load = data.copy()
        data_to_load['cd_customer'] = customer_id
        data_to_load['cd_user'] = user_id
        
        # 3. Validar os dados com o esquema
        interaction = interaction_schema.load(data_to_load, session=db.session)
        
        # 4. Salvar no *nosso* banco de dados
        db.session.add(interaction)
        db.session.commit()
        return interaction
    except ValidationError as err:
        raise InvalidDataError(err.messages)

def get_interactions_for_customer(customer_id, page=1, per_page=15):
    """Retorna uma lista paginada de interações para um cliente específico."""
    
    # 1. Validar que o cliente existe antes de fazer a busca
    _validate_customer_exists(customer_id)
        
    # 2. Buscar no *nosso* banco de dados
    paginated = Interaction.query.filter_by(cd_customer=customer_id)\
        .order_by(Interaction.dt_interaction.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
        
    return paginated

# --- LÓGICA DE TRANSAÇÃO (VOCÊ PODE ADICIONAR create_transaction, etc. aqui) ---
# ... (O padrão seria idêntico: validar cliente, validar usuário, salvar no DB)
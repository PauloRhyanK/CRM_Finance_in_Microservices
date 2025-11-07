# /gateway/app.py
import os
import requests
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

SERVICE_MAP = {
    'auth': app.config['AUTH_SERVICE_URL'],
    'customers': app.config['CUSTOMER_SERVICE_URL'],
    'products': app.config['PRODUCT_SERVICE_URL'],
    'interactions': app.config['INTERACTION_SERVICE_URL'] 
    # ^^^ NOTE: O interaction service está aninhado sob /customers no gateway
}

# --- Rota Catch-All ---
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def gateway(path):
    """
    Rota principal que captura todas as requisições e as encaminha
    para o microserviço apropriado.
    """
    service_name = None
    service_path = path
    
    # 1. Determinar o serviço de destino com base no início do path
    # Ex: /auth/login -> service_name='auth', service_path='login'
    # Ex: /api/customers/123 -> service_name='customers', service_path='123'
    # Ex: /api/customers/123/interactions -> service_name='interactions', service_path='123/interactions'

    parts = path.split('/')
    
    if path.startswith('auth'):
        service_name = 'auth'
        service_path = path 
    elif path.startswith('api/customers'):
        if len(parts) > 3 and parts[3] == 'interactions':
             # Rota aninhada: /api/customers/{id}/interactions -> interaction_service
             service_name = 'interactions'
             # O serviço de interação espera a rota no formato /{customer_id}/interactions
             service_path = path
        else:
             # Rota de cliente normal: /api/customers/... -> customer_service
             service_name = 'customers'
             service_path = path
    elif path.startswith('api/products'):
        service_name = 'products'
        service_path = path
    
    if not service_name or service_name not in SERVICE_MAP:
        return jsonify({'error': 'Serviço não encontrado'}), 404

    service_url = SERVICE_MAP[service_name]
    downstream_url = f"{service_url}/{service_path}"

    # 2. Verificar autenticação (se não for rota de auth)
    user_id = None
    if service_name != 'auth':
        try:
            # Verifica se há um token JWT válido na requisição
            verify_jwt_in_request() 
            # Se for válido, pega o ID do usuário ('identity' que definimos no auth-service)
            user_id = get_jwt_identity() 
        except Exception as e:
            # Se o token for inválido ou ausente, retorna erro 401
            return jsonify({'error': 'Token de autenticação inválido ou ausente'}), 401

    # 3. Preparar e encaminhar a requisição
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    # Adiciona o X-User-Id se autenticado (crucial para o interaction-service)
    if user_id:
        headers['X-User-Id'] = user_id
        
    try:
        resp = requests.request(
            method=request.method,
            url=downstream_url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            stream=True,    # Importante para lidar com grandes respostas
            timeout=30      # Timeout de 30 segundos
        )

        # 4. Retornar a resposta do microserviço para o cliente original
        response_headers = [(name, value) for (name, value) in resp.raw.headers.items() 
                            if name.lower() not in ['content-encoding', 'transfer-encoding', 'connection']]

        response = (resp.content, resp.status_code, response_headers)
        return response

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro ao conectar ao serviço {service_name}: {e}'}), 503 # Service Unavailable

if __name__ == '__main__':
    # O gateway roda na porta 8080 por padrão
    port = int(os.environ.get('PORT', 8080)) 
    app.run(host='0.0.0.0', port=port)
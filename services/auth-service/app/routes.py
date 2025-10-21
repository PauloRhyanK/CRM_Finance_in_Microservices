# /auth-service/app/routes.py
from flask import Blueprint, request, jsonify
from . import services
from .schemas import UserSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado enviado"}), 400

    new_user = services.register_new_user(form_data=data)
    return jsonify({
        "message": "Usuário registrado com sucesso!",
        "user": user_schema.dump(new_user)
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado enviado"}), 400

    token, user = services.authenticate_user(form_data=data)
    
    return jsonify({
        "message": "Login bem-sucedido.",
        "access_token": token,
        "user": user_schema.dump(user)
    }), 200
from flask import Blueprint, jsonify, request

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify({"message": "List of users"}), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({"message": f"User {user_id} details"}), 200

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify({"message": "User created", "data": data}), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    return jsonify({"message": f"User {user_id} updated", "data": data}), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return jsonify({"message": f"User {user_id} deleted"}), 204
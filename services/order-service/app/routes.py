from flask import Blueprint, request, jsonify

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    # Logic to create an order
    return jsonify({"message": "Order created", "data": data}), 201

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # Logic to retrieve an order by ID
    return jsonify({"message": "Order retrieved", "order_id": order_id}), 200

@order_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    # Logic to update an order
    return jsonify({"message": "Order updated", "order_id": order_id, "data": data}), 200

@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Logic to delete an order
    return jsonify({"message": "Order deleted", "order_id": order_id}), 204
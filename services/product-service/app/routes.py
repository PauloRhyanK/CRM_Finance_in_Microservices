from flask import Blueprint, jsonify, request

product_bp = Blueprint('product', __name__)

# Sample in-memory product storage
products = []

@product_bp.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200

@product_bp.route('/products', methods=['POST'])
def create_product():
    product_data = request.json
    products.append(product_data)
    return jsonify(product_data), 201

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    if 0 <= product_id < len(products):
        return jsonify(products[product_id]), 200
    return jsonify({'error': 'Product not found'}), 404

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if 0 <= product_id < len(products):
        product_data = request.json
        products[product_id] = product_data
        return jsonify(product_data), 200
    return jsonify({'error': 'Product not found'}), 404

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 0 <= product_id < len(products):
        deleted_product = products.pop(product_id)
        return jsonify(deleted_product), 200
    return jsonify({'error': 'Product not found'}), 404
from flask import Blueprint, jsonify

product_bp = Blueprint('products', __name__)

@product_bp.route('/', methods=['GET'])
def list_products():
    return jsonify({"message": "Listado de productos"}), 200

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return jsonify({"message": f"Detalles del producto {product_id}"}), 200

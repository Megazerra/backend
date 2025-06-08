from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.models import Product

product_bp = Blueprint('products', __name__)

@product_bp.route('/', methods=['GET'])
def list_products():
    products = Product.query.all()
    result = []

    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock": p.stock,
            "image_url": p.image_url
        })

    return jsonify(result), 200

@product_bp.route('/<int:product_id>', methods=['GET'])
def product(product_id):
    producto = Product.query.get(product_id)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({
        "id": producto.id,
        "name": producto.name,
        "description": producto.description,
        "price": producto.price,
        "stock": producto.stock,
        "image_url": producto.image_url
    }), 200

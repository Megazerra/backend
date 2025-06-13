from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from flask import Blueprint, jsonify, request
from app.models import CartItem

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([i.to_dict() for i in items]), 200

@cart_bp.route('', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    product_data = data.get('product')
    if not product_data:
        return jsonify({'msg': 'Falta el producto'}), 400

    # Extrae campos del objeto product
    product_id = product_data.get('id')
    if product_id is None:
        return jsonify({'msg': 'Falta el id de producto'}), 400

    name = product_data.get('name', '')
    price = product_data.get('price', 0)
    quantity = data.get('quantity', 1)
    image_url = product_data.get('image_url') or product_data.get('imageUrl')

    # Busca ítem existente
    item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItem(
            user_id=user_id,
            product_id=product_id,
            name=name,
            price=price,
            quantity=quantity,
            image_url=image_url
        )
        db.session.add(item)

    db.session.commit()
    return jsonify(item.to_dict()), 201

@cart_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(product_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first_or_404()

    if 'quantity' in data:
        item.quantity = data['quantity']
        db.session.commit()
    return jsonify(item.to_dict()), 200

@cart_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_item(product_id):
    user_id = get_jwt_identity()
    item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first_or_404()

    db.session.delete(item)
    db.session.commit()
    return '', 204
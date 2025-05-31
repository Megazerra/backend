from flask import Blueprint, jsonify

order_bp = Blueprint('orders', __name__)

@order_bp.route('/', methods=['GET'])
def list_orders():
    return jsonify({"message": "Listado de pedidos"}), 200

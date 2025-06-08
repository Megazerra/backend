from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, get_jwt, \
    get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User

auth_bp = Blueprint('users', __name__)

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user: User = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    resp = jsonify({
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    })

    return resp, 200

@auth_bp.route('/update', methods=['PUT'])
@jwt_required()
def update():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    profile_image = data.get('profile_image')

    if name:
        user.name = name
    if email:
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user.id:
            return jsonify({"error": "Ese email ya está en uso"}), 409
        user.email = email
    if password:
        user.password = generate_password_hash(password)
    if profile_image:
        user.profile_image = profile_image

    db.session.commit()

    return jsonify({"message": "Usuario actualizado correctamente"}), 200

@auth_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado correctamente"}), 200


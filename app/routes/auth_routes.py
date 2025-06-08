from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, get_jwt, \
    get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña requeridos"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Crear token JWT
    access_token = create_access_token(identity=str(user.id))
    resp = jsonify({
        "message": "Inicio de sesión exitoso",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    })
    set_access_cookies(resp, access_token)

    return resp, 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = jsonify(logout=True)
    unset_jwt_cookies(resp)
    return resp

@auth_bp.route('/test', methods=['POST'])
@jwt_required()
def test():
    data = request.get_json()
    msg = data.get('msg', '')

    jwt_data = get_jwt()
    identity = get_jwt_identity()
    exp_timestamp = jwt_data.get('exp')
    exp_datetime = datetime.utcfromtimestamp(exp_timestamp).isoformat() + 'Z'

    return jsonify({
        'message': f'Test pasado: {msg}',
        'user_id': identity,
        'expires_at': exp_datetime,
        'jwt_payload': jwt_data
    }), 200

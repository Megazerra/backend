from flask import jsonify

def register_jwt_callbacks(jwt):
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "token_expired",
            "description": "El token ha caducado. Por favor, vuelve a iniciar sesión."
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({
            "error": "invalid_token",
            "description": reason
        }), 422

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return jsonify({
            "error": "authorization_missing",
            "description": reason
        }), 401
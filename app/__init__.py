from datetime import timedelta
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

from flask import Flask
from app.extensions import db, migrate, login_manager, jwt
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, origins=["http://localhost:4200"])

    # Configuración JWT
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=30)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Importaciones tardías para evitar ciclos
    from app.routes.auth_routes import auth_bp
    from app.routes.product_routes import product_bp
    from app.routes.order_routes import order_bp
    from app.routes.user_routes import users_bp

    from app.auxiliar.interceptor import register_jwt_callbacks

    # Registrar Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(users_bp, url_prefix='/api/users')


    # Registrar callbacks de JWT
    register_jwt_callbacks(jwt)

    return app

from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import Config

# 1. Instanciamos extensiones (globales pero sin app)
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    # 2. Inicializamos las extensiones con la app
    db.init_app(application)
    ma.init_app(application)
    jwt.init_app(application)

    # Flask Error Handlers - catch all exceptions and log them
    @application.errorhandler(Exception)
    def handle_all_errors(error):
        # Log the error for debugging
        application.logger.error(f"Unhandled exception: {type(error).__name__}: {str(error)}")
        
        # Check if it's a NoAuthorizationError by class name
        if "NoAuthorizationError" in type(error).__name__:
            return jsonify({"msg": "Missing Authorization Header"}), 401
        
        # Default to 500
        return jsonify({"msg": "Internal server error"}), 500
    
    # 3. Importar modelos antes de inicializar Migrate
    # Esto permite que Alembic (el motor de Migrate) vea las tablas
    from .models import Blacklist 
    migrate.init_app(application, db)

    # 4. Configuración de API y Rutas
    from .resources import BlacklistResource, HealthCheck
    api = Api(application)
    
    api.add_resource(BlacklistResource, '/blacklists', '/blacklists/<email>')
    api.add_resource(HealthCheck, '/health')

    return application
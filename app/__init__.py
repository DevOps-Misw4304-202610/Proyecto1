from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import Config

# Inicializamos extensiones sin "atarlas" aún a la app
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    application = Flask(__name__)
    application.config.from_object(Config)

    db.init_app(application)
    ma.init_app(application)
    jwt.init_app(application)
    migrate.init_app(application, db)

    from .resources import BlacklistResource, HealthCheck
    api = Api(application)
    
    # Rutas
    api.add_resource(BlacklistResource, '/blacklists')
    api.add_resource(HealthCheck, '/health')

    return application
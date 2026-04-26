import pytest
from app import create_app
from app.config import Config
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    class TestConfig(Config):
        TESTING = True
        # Ya no es necesaria una base de datos real para mocks, 
        # pero mantenemos la estructura de configuración.
        SQLALCHEMY_DATABASE_URI = "sqlite://" 

    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_header(app):
    with app.app_context():
        # Genera un token para las pruebas de seguridad
        token = create_access_token(identity="test_user")
        return {"Authorization": f"Bearer {token}"}
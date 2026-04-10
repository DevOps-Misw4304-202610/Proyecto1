import pytest
from app import create_app, db
from app.config import Config
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_header(app):
    with app.app_context():
        token = create_access_token(identity="test_user")
        return {"Authorization": f"Bearer {token}"}
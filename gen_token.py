import os
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
from dotenv import load_dotenv

# Cargamos el .env para usar la misma SECRET_KEY que el servidor
load_dotenv()

application = Flask(__name__)
application.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-secret")
jwt = JWTManager(application)

with application.app_context():
    # Creamos un token que expire en 10 años (estático para fines prácticos)
    expires = timedelta(days=3650)
    token = create_access_token(identity="admin_system", expires_delta=expires)
    
    print("\n" + "="*50)
    print("TOKEN ESTÁTICO GENERADO:")
    print("="*50)
    print(f"\nBearer {token}\n")
    print("="*50)
    print("Copia este string (incluyendo la palabra Bearer) para tus pruebas en Postman.\n")
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .models import db, Blacklist
from .schemas import BlacklistSchema

# Instanciamos el schema para validar entradas
blacklist_schema = BlacklistSchema()

class HealthCheck(Resource):
    def get(self):
        return {"status": "UP"}, 200

class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        
        # Validar datos con Marshmallow
        errors = blacklist_schema.validate(data)
        if errors:
            return errors, 400

        # Crear la entrada
        new_entry = Blacklist(
            email=data['email'],
            app_uuid=data['app_uuid'],
            blocked_reason=data.get('blocked_reason'),
            ip_address=request.remote_addr
        )
        
        try:
            db.session.add(new_entry)
            db.session.commit()
            return {"msg": "Email added to blacklist successfully", "id": new_entry.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": "Database error", "error": str(e)}, 500
from flask import request
from flask_restful import Resource
from .models import db, Blacklist
from flask_jwt_extended import jwt_required
from .models import db, Blacklist
from .schemas import BlacklistSchema
from sqlalchemy.exc import IntegrityError

# Instanciamos el schema para validar entradas
blacklist_schema = BlacklistSchema()

class HealthCheck(Resource):
    def get(self):
        return {"status": "UP"}, 200

class BlacklistResource(Resource):
    @jwt_required()
    def get(self, email):
        # Consultamos siempre en minúsculas
        blacklist_entry = Blacklist.query.filter_by(email=email.lower()).first()
        
        if blacklist_entry:
            return {
                "present": True,
                "blocked_reason": blacklist_entry.blocked_reason or ""
            }, 200
        return {"present": False, "blocked_reason": ""}, 200
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        errors = blacklist_schema.validate(data)
        if errors:
            return errors, 400

        # Normalizamos a minúsculas antes de crear el objeto
        new_entry = Blacklist(
            email=data['email'].lower(), 
            app_uuid=data['app_uuid'],
            blocked_reason=data.get('blocked_reason'),
            ip_address=request.remote_addr
        )
        
        try:
            db.session.add(new_entry)
            db.session.commit()
            return {"msg": "Email added to blacklist successfully", "id": new_entry.id}, 201
        except IntegrityError:
            db.session.rollback()
            return {"msg": "Email already exists in blacklist"}, 400 # O 409 Conflict
        except Exception as e:
            db.session.rollback()
            return {"msg": str(e)}, 500
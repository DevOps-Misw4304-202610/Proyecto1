from flask import request
from flask_restful import Resource
from .models import db, Blacklist
from flask_jwt_extended import jwt_required
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
        """Get blacklist status for an email"""
        try:
            # Consultamos siempre en minúsculas
            blacklist_entry = Blacklist.query.filter_by(email=email.lower()).first()
            
            if blacklist_entry:
                return {
                    "present": True,
                    "blocked_reason": blacklist_entry.blocked_reason or ""
                }, 200
            return {"present": False, "blocked_reason": ""}, 200
        except Exception as e:
            return {"msg": f"Error querying blacklist: {str(e)}"}, 500
    
    @jwt_required()
    def post(self):
        """Add email to blacklist"""
        data = request.get_json()
        
        # Validate input data
        errors = blacklist_schema.validate(data)
        if errors:
            return {"errors": errors}, 400  # Keep 400 for consistency with tests
        
        try:
            # Normalize email to lowercase
            email_normalized = data['email'].lower()
            
            # Create new blacklist entry
            new_entry = Blacklist(
                email=email_normalized, 
                app_uuid=data['app_uuid'],
                blocked_reason=data.get('blocked_reason'),
                ip_address=request.remote_addr  # Get IP from request
            )
            
            # Add and commit to database
            db.session.add(new_entry)
            db.session.commit()
            
            # Return success with created entry ID
            return {
                "msg": "Email added to blacklist successfully", 
                "id": new_entry.id,
                "email": new_entry.email
            }, 201
            
        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg": "Email already exists in blacklist",
                "error": "DUPLICATE_EMAIL"
            }, 409  # Conflict
        except Exception as e:
            db.session.rollback()
            return {
                "msg": f"Error adding to blacklist: {str(e)}"
            }, 500
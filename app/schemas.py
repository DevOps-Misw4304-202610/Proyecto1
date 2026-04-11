# app/schemas.py
from . import ma
from .models import Blacklist
from marshmallow import fields, validate

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        load_instance = True
        # Exclude auto-generated fields from input
        exclude = ('id', 'createdAt', 'ip_address')

    # Email validation
    email = fields.String(
        required=True, 
        validate=validate.Email(error="Formato de email inválido.")
    )
    
    # Required fields
    app_uuid = fields.String(
        required=True,
        validate=validate.Length(min=1, max=36, error="app_uuid must be 1-36 characters")
    )
    
    # Optional field
    blocked_reason = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=255)
    )
    
    # Output only - server-generated
    ip_address = fields.String(dump_only=True)
# app/schemas.py
from . import ma
from .models import Blacklist
from marshmallow import fields, validate

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        load_instance = True

    # Cambia validate.Regexp por validate.Email()
    email = fields.String(
        required=True, 
        validate=validate.Email(error="Formato de email inválido.")
    )
    app_uuid = fields.String(required=True)
    blocked_reason = fields.String(validate=validate.Length(max=255))
    ip_address = fields.String(dump_only=True)
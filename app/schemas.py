from . import ma
from .models import Blacklist
from marshmallow import fields, validate

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        load_instance = True

    # Validaciones personalizadas
    email = fields.String(required=True, validate=validate.Email())
    app_uuid = fields.String(required=True)
    blocked_reason = fields.String(validate=validate.Length(max=255))
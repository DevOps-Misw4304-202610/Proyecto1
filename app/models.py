from datetime import datetime, timezone
from . import db

class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    # Añadimos unique=True
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=False)
    createdAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
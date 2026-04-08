from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
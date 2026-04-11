import os
from dotenv import load_dotenv

load_dotenv()


def _get_database_uri():
    """
    Get database URI based on configuration.
    
    If RDS_HOSTNAME is set, uses AWS RDS IAM authentication.
    Otherwise, falls back to DATABASE_URL environment variable.
    """
    # Check if using AWS RDS with IAM auth
    if os.getenv('RDS_HOSTNAME'):
        try:
            from .aws_rds import build_rds_database_uri
            return build_rds_database_uri()
        except Exception as e:
            print(f"Warning: Failed to build RDS URI: {e}. Falling back to DATABASE_URL")
            return os.getenv('DATABASE_URL', 'postgresql+psycopg://user_blacklist:password123@localhost:5433/blacklist_db')
    
    # Fall back to standard DATABASE_URL
    return os.getenv('DATABASE_URL', 'postgresql+psycopg://user_blacklist:password123@localhost:5433/blacklist_db')


class Config:
    SQLALCHEMY_DATABASE_URI = _get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'una-clave-super-larga-y-segura-de-mas-de-32-caracteres')
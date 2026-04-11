import os
import boto3
from botocore.exceptions import ClientError


def get_rds_auth_token():
    """
    Generate a temporary AWS RDS authentication token for IAM database authentication.
    
    This function uses boto3 to generate a secure token that serves as the password
    for connecting to RDS. The token is temporary and expires after 15 minutes.
    
    Environment variables required:
    - RDS_HOSTNAME: RDS endpoint (e.g., database-1.cluster-xxxxx.us-east-1.rds.amazonaws.com)
    - RDS_PORT: PostgreSQL port (default: 5432)
    - RDS_USERNAME: DB username (typically 'postgres')
    - AWS_REGION: AWS region (e.g., us-east-1)
    - AWS_ACCESS_KEY_ID: AWS access key (optional if using IAM role)
    - AWS_SECRET_ACCESS_KEY: AWS secret key (optional if using IAM role)
    
    Returns:
        str: Authentication token to use as password for RDS connection
        
    Raises:
        ClientError: If token generation fails (check AWS credentials and permissions)
    """
    try:
        rds_hostname = os.getenv('RDS_HOSTNAME')
        rds_port = os.getenv('RDS_PORT', '5432')
        rds_username = os.getenv('RDS_USERNAME', 'postgres')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        # Validate required environment variables
        if not rds_hostname:
            raise ValueError("RDS_HOSTNAME environment variable not set")
        
        # Create RDS client
        client = boto3.client('rds', region_name=aws_region)
        
        # Generate auth token (valid for 15 minutes)
        token = client.generate_db_auth_token(
            DBHostname=rds_hostname,
            Port=int(rds_port),
            DBUsername=rds_username,
            Region=aws_region
        )
        
        return token
    except ClientError as e:
        raise Exception(f"Failed to generate RDS auth token: {e}")
    except Exception as e:
        raise Exception(f"Error in token generation: {e}")


def build_rds_database_uri():
    """
    Build the database connection URI for AWS RDS with IAM authentication.
    
    This function constructs a PostgreSQL connection string using the temporary
    auth token from AWS RDS IAM database authentication.
    
    Environment variables required:
    - RDS_HOSTNAME: RDS endpoint
    - RDS_PORT: PostgreSQL port (default: 5432)
    - RDS_USERNAME: DB username
    - RDS_DB_NAME: Database name
    - AWS_REGION: AWS region
    
    Returns:
        str: PostgreSQL connection URI
    """
    try:
        rds_hostname = os.getenv('RDS_HOSTNAME')
        rds_port = os.getenv('RDS_PORT', '5432')
        rds_username = os.getenv('RDS_USERNAME', 'postgres')
        rds_db_name = os.getenv('RDS_DB_NAME', 'postgres')
        
        # Generate auth token
        auth_token = get_rds_auth_token()
        
        # Build URI with SSL requirement for AWS
        database_uri = (
            f"postgresql+psycopg://{rds_username}:{auth_token}@"
            f"{rds_hostname}:{rds_port}/{rds_db_name}?sslmode=require"
        )
        
        return database_uri
    except Exception as e:
        raise Exception(f"Failed to build RDS database URI: {e}")

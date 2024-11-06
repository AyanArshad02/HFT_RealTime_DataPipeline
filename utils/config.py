import os
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Configuring database using environment variables
DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

DATABASE_CONFIG = {
    'POSTGRES_URL': f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
}

MLFLOW_TRACKING_URI = "http://localhost:5000"


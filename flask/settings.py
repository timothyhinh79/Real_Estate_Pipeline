import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_DATABASE_SCHEMA = os.getenv('POSTGRES_DATABASE_SCHEMA')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
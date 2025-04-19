from backend.config import DB_CONFIG
import psycopg2

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

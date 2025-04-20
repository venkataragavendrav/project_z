from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "POSTGRES_DB": os.getenv("POSTGRES_DB"),
    "POSTGRES_USER": os.getenv("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
    "POSTGRES_PORT": os.getenv("POSTGRES_PORT")
}

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

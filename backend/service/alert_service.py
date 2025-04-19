import psycopg2
import requests
from datetime import datetime

from backend.service.db_utils import get_db_connection

def insert_alert(alert_type, description, severity, run_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO alerts (alert_type, description, severity, run_id, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            alert_type,
            description,
            severity,
            run_id,
            datetime.utcnow()
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Alert inserted into database.")
    except Exception as e:
        print("❌ Failed to insert alert:", str(e))


def send_slack_alert(message, webhook_url):
    try:
        response = requests.post(
            webhook_url,
            json={"text": message},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Slack alert sent successfully.")
        else:
            print("❌ Slack alert failed:", response.text)
    except Exception as e:
        print("❌ Error sending Slack alert:", str(e))
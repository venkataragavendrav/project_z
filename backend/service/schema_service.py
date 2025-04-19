import psycopg2
import json

from backend.service.db_utils import get_db_connection

def insert_schema_snapshot(schema_dict, datasource, table_name, change_detected):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO schema_versions (datasource, table_name, detected_schema, change_detected)
        VALUES (%s, %s, %s, %s)
    """, (
        datasource,
        table_name,
        json.dumps(schema_dict),
        change_detected
    ))
    conn.commit()
    cursor.close()
    conn.close()

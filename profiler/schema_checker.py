from backend.service.db_utils import get_db_connection

def get_schema_snapshot(df):
    return {field.name: str(field.dataType) for field in df.schema.fields}


def detect_schema_drift(current_schema: dict, previous_schema: dict):
    drift = {"added": [], "removed": [], "type_changed": []}

    current_cols = set(current_schema.keys())
    previous_cols = set(previous_schema.keys())

    drift["added"] = list(current_cols - previous_cols)
    drift["removed"] = list(previous_cols - current_cols)

    for col in current_cols & previous_cols:
        if current_schema[col] != previous_schema[col]:
            drift["type_changed"].append(col)

    return drift

def fetch_latest_schema_snapshot(datasource, table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT detected_schema FROM schema_versions 
        WHERE datasource = %s AND table_name = %s 
        ORDER BY detected_on DESC LIMIT 1
    """, (datasource, table_name))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return json.loads(row[0]) if row else None

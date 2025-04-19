from backend.service.db_utils import get_db_connection

def insert_into_data_profile(profiles, run_id, datasource, table_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    for profile in profiles:
        cursor.execute("""
            INSERT INTO data_profile 
            (datasource, table_name, profile_date, column_name, null_percentage, distinct_count, duplicate_count, min_value, max_value, run_id)
            VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s)
        """, (
            datasource,
            table_name,
            profile["column_name"],
            profile["null_percentage"],
            profile["distinct_count"],
            profile["duplicate_count"],
            str(profile["min_value"]) if profile["min_value"] is not None else None,
            str(profile["max_value"]) if profile["max_value"] is not None else None,
            run_id
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Profiling data inserted successfully.")
from backend.service.db_utils import get_db_connection

def execute_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql = file.read()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("❌ Error running SQL:", e)

    cursor.close()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    execute_sql_file("../sql/create_tables.sql")

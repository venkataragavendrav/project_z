import psycopg2

def execute_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql = file.read()

    conn = psycopg2.connect(
        dbname="project_z",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    execute_sql_file("../sql/create_tables.sql")

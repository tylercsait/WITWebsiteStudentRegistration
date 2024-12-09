from datetime import datetime, date
import mysql.connector
from mysql.connector import errorcode
from contextlib import contextmanager

"This code contains methods to use the DB"

config = {
    'host': 'wit-sql.mysql.database.azure.com',
    'user': 'witadmin',
    'password': 'qpwoei102938!',
    'database': 'wit'
    # 'client_flags': [mysql.connector.ClientFlag.SSL],
    # 'ssl_ca': '<path-to-SSL-cert>/DigiCertGlobalRootG2.crt.pem'
}

def close_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Connection closed.")

@contextmanager
def mysql_connection():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**config)
        print("Connection established")
        cursor = connection.cursor(buffered=True)  # Use a buffered cursor
        yield cursor
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        close_connection(connection, cursor)

def __create_table(cursor, table_name, create_query):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    print(f"Finished dropping {table_name} table (if existed).")
    cursor.execute(create_query)
    print(f"Finished creating {table_name} table.")

def __get_column_value(cursor, table, column, student_id):
    query = f"SELECT {column} FROM {table} WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def create_students_table(cursor):
    create_query = """
    CREATE TABLE students (
        student_id VARCHAR(50) PRIMARY KEY,
        student_name VARCHAR(50)
    );
    """
    __create_table(cursor, "students", create_query)

def view_table(cursor, table_name):
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def delete_student_by_id(cursor, student_id):
    delete_query = "DELETE FROM students WHERE student_id = %s"
    cursor.execute(delete_query, (student_id,))
    print("Deleted", cursor.rowcount, f"{student_id}")

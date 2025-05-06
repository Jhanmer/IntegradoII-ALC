# app/config.py

import psycopg2

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123', 
            dbname='stock_system'  
        )
        return connection
    except Exception as ex:
        print("Error de conexión:", ex)
        return None

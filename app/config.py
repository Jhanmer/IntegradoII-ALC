# app/config.py

import psycopg2
# Importar os puede ser útil si luego quieres usar variables de entorno, pero no es estrictamente necesario para la depuración con valores fijos
# import os

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='12345',
            dbname='stock_system'
        )
        # --- AÑADE ESTA LÍNEA AQUÍ ---
        print(f"DEBUG: Conexión DB -> DBNAME={connection.get_dsn_parameters().get('dbname')} HOST={connection.get_dsn_parameters().get('host')} PORT={connection.get_dsn_parameters().get('port')} USER={connection.get_dsn_parameters().get('user')}")
        # -----------------------------
        return connection
    except psycopg2.OperationalError as e: # Usar OperationalError es más específico para problemas de conexión
        print(f"DEBUG: Error de conexión a la base de datos: {e}")
        return None # O podrías considerar lanzar una excepción para que el error sea más visible
    except Exception as ex: # Captura otras posibles excepciones durante la conexión
        print(f"DEBUG: Ocurrió un error inesperado al conectar a la base de datos: {ex}")
        return None
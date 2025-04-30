import psycopg2

try:
    connection=psycopg2.connect(
        host='localhost',
        user='postgres',
        password='123',
        database='BD_GestionInventarioPrdc'
    )
    print("Conexión exitosa")
except Exception as ex:
    print(ex)
import psycopg2
from datetime import datetime, timedelta
import random

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="stock_system",
    user="postgres",
    password="123"
)
cur = conn.cursor()

# Obtener todos los ID de productos existentes
cur.execute("SELECT id FROM productos")
producto_ids = [row[0] for row in cur.fetchall()]

if not producto_ids:
    print("No se encontraron productos en la base de datos.")
    cur.close()
    conn.close()
    exit()

# Fechas de inicio y fin (enero y febrero de 2021)
start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 2, 28)

current_date = start_date

while current_date <= end_date:
    # Generar entre 3 y 10 pedidos por día
    for _ in range(random.randint(3, 10)):
        supervisor_id = random.randint(1, 5)
        producto_id = random.choice(producto_ids)
        cantidad = random.randint(1, 20)

        # Insertar pedido con la fecha exacta del día (sin hora)
        cur.execute("""
            INSERT INTO pedidos (supervisor_id, producto_id, cantidad, fecha)
            VALUES (%s, %s, %s, %s)
        """, (supervisor_id, producto_id, cantidad, current_date))

    current_date += timedelta(days=1)

conn.commit()
cur.close()
conn.close()

print("Pedidos generados correctamente para enero y febrero de 2021.")

# app/models/producto.py

from app.config import get_db_connection

def obtener_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos ORDER BY id DESC")
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

def insertar(datos):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO productos (descripcion, sku, marca, proveedor, division, estado, oh_disponible, nuevo_oh)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, datos)
    conn.commit()
    cur.close()
    conn.close()

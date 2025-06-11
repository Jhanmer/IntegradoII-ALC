# app/models/producto.py

from app.config import get_db_connection

def obtener_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.id,
            p.descripcion,
            p.sku,
            m.nombre AS marca,
            pr.nombre AS proveedor,
            p.division,
            p.estado,
            p.oh_disponible,
            p.nuevo_oh
        FROM productos p
        LEFT JOIN marcas m ON p.marca_id = m.id
        LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
        ORDER BY p.id ASC
    """)
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados


def insertar(datos):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO productos (
            descripcion, sku, marca_id, proveedor_id, division,
            estado, oh_disponible, nuevo_oh
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, datos)
    conn.commit()
    cur.close()
    conn.close()



def insertar_marca(nombre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO marcas (nombre) VALUES (%s)", (nombre,))
    conn.commit()
    cur.close()
    conn.close()

def obtener_marcas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM marcas ORDER BY nombre ASC")
    marcas = cur.fetchall()
    cur.close()
    conn.close()
    return marcas


def agregar_proveedor(nombre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO proveedores (nombre) VALUES (%s)", (nombre,))
    conn.commit()
    cur.close()
    conn.close()

def obtener_proveedores():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM proveedores ORDER BY nombre ASC")
    proveedores = cur.fetchall()
    cur.close()
    conn.close()
    return proveedores

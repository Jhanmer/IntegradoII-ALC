from app.config import get_db_connection

def obtener_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.id,
            p.descripcion,
            p.sku,
            COALESCE(m.nombre, 'Sin Marca') AS marca,
            COALESCE(pr.nombre, 'Sin Proveedor') AS proveedor,
            p.division,
            p.estado,
            p.oh_disponible,
            p.nuevo_oh,
            (p.oh_disponible + p.nuevo_oh) AS stock_total
        FROM productos p
        LEFT JOIN marcas m ON p.marca_id = m.id
        LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
        ORDER BY p.id ASC
    """)
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

def descripcion_existe(descripcion):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM productos WHERE LOWER(descripcion) = LOWER(%s)", (descripcion,))
    existe = cur.fetchone()[0] > 0
    cur.close()
    conn.close()
    return existe

def insertar_o_actualizar(datos):
    descripcion, sku, marca_id, proveedor_id, division, estado, oh_disponible, nuevo_oh = datos
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Verificar existencia del producto por SKU
        cur.execute("SELECT id, oh_disponible, nuevo_oh FROM productos WHERE sku = %s", (sku,))
        existente = cur.fetchone()

        if existente:
            producto_id, oh_actual, nuevo_actual = existente

            nuevo_oh_total = nuevo_actual + nuevo_oh
            nuevo_oh_disponible_total = oh_actual + nuevo_oh

            cur.execute("""
                UPDATE productos
                SET 
                    nuevo_oh = %s,
                    oh_disponible = %s
                WHERE id = %s
            """, (nuevo_oh_total, nuevo_oh_disponible_total, producto_id))

        else:
            cur.execute("""
                INSERT INTO productos (
                    descripcion, sku, marca_id, proveedor_id, division,
                    estado, oh_disponible, nuevo_oh
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (descripcion, sku, marca_id, proveedor_id, division, estado, oh_disponible, nuevo_oh))

        conn.commit()

    except Exception as e:
        print("🛑 Error en insertar_o_actualizar:", e)
        raise

    finally:
        cur.close()
        conn.close()

def actualizar_stock_por_sku(sku, nuevo_oh_sumar):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM productos WHERE sku = %s", (sku,))
    producto = cur.fetchone()

    if producto:
        producto_id = producto[0]
        cur.execute("""
            UPDATE productos
            SET nuevo_oh = nuevo_oh + %s
            WHERE id = %s
        """, (nuevo_oh_sumar, producto_id))
        conn.commit()

    cur.close()
    conn.close()

def obtener_descripciones():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT sku, descripcion FROM productos ORDER BY descripcion ASC")
    descripciones = cur.fetchall()
    cur.close()
    conn.close()
    return descripciones

def insertar_marca(nombre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM marcas WHERE LOWER(nombre) = LOWER(%s)", (nombre,))
    existe = cur.fetchone()
    if not existe:
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

def obtener_marca_por_nombre(nombre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM marcas WHERE LOWER(nombre) = LOWER(%s)", (nombre,))
    marca = cur.fetchone()
    cur.close()
    conn.close()
    return marca


def agregar_proveedor(nombre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO proveedores (nombre) VALUES (%s)", (nombre,))
    conn.commit()
    cur.close()
    conn.close()

def obtener_proveedor_por_nombre(nombre):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM proveedores WHERE LOWER(nombre) = LOWER(%s)", (nombre,))
    proveedor = cur.fetchone()
    cur.close()
    conn.close()
    return proveedor

def obtener_proveedores():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM proveedores ORDER BY nombre ASC")
    proveedores = cur.fetchall()
    cur.close()
    conn.close()
    return proveedores

def obtener_productos_sku_descripcion():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT sku, descripcion FROM productos ORDER BY descripcion ASC")
    datos = cur.fetchall()
    cur.close()
    conn.close()
    return datos

def descripcion_existe(descripcion):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM productos WHERE LOWER(descripcion) = LOWER(%s) LIMIT 1", (descripcion,))
    existe = cur.fetchone() is not None
    cur.close()
    conn.close()
    return existe
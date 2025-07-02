-- Database: stock_system

DROP DATABASE IF EXISTS stock_system;

CREATE DATABASE stock_system
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es-PE'
    LC_CTYPE = 'es-PE'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

\c stock_system;
--MOVER HACIA LA CONEXION DE LA BASE DE DATOS
-- Tabla de marcas
CREATE TABLE marcas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de proveedores
CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

--Tabla de usuarios
CREATE TABLE usuario (
    CodUsu INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    login VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo'
);

-- Tabla de productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    sku CHAR(8) UNIQUE NOT NULL,
    marca_id INT,
    proveedor_id INT,
    supervisor_id INT,  -- NUEVO: usuario que registró el producto
    division VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,
    oh_disponible INTEGER DEFAULT 0,
    nuevo_oh INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_marca FOREIGN KEY (marca_id) REFERENCES marcas(id) ON DELETE SET NULL,
    CONSTRAINT fk_proveedor FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE SET NULL,
    CONSTRAINT fk_supervisor FOREIGN KEY (supervisor_id) REFERENCES usuario(CodUsu) ON DELETE SET NULL
);

select * from proveedores
select * from marcas
select * from productos

-- Insertar datos en la tabla 'usuario'

INSERT INTO usuario (nombre, rol, login, password, estado)
VALUES
    ('Yarel Auqui',    'administrador', 'yauqui@alicorp.pe',   'utp', 'activo'),
    ('Eduardo Quiroz', 'supervisor',    'equiroz@alicorp.pe',  'utp', 'activo'),
    ('Miguel Guillen', 'mercader',      'mguillen@alicorp.pe', 'utp', 'activo'),
    ('Amir Rivero',    'supervisor',    'arivero@alicorp.pe',  'utp', 'activo'),
    ('Jhanmer Paucar', 'almacen',       'jpaucar@alicorp.pe',  'utp', 'activo');

select * from usuario;

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    supervisor_id INT REFERENCES usuario(CodUsu),
    producto_id INT REFERENCES productos(id),
    cantidad INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos en la tabla 'marcas'
INSERT INTO marcas (nombre) VALUES
('Alicorp'),
('Backus y Johnston'),
('Inca Kola'),
('Donofrio'),
('Laive'),
('Sol Alpaca'),
('Dunkelvolk'),
('Incas Food'),
('Camposol'),
('Cerro Verde'),
('Gloria'), 
('Ajegroup'), 
('Kuna'), 
('Campomar'); 

-- Insertar datos en la tabla 'proveedores'
INSERT INTO proveedores (nombre) VALUES
('Michell & Co.'),
('Art Atlas S.R.L.'),
('Kusa Cotton Peru'),
('Frozen Products Corporation'),
('Marex'),
('Peimco'),
('Berrocal'),
('Antamina'),
('Southern Peru Copper Corporation'),
('Agrokasa'),
('DanPer'), 
('Hortifrut Perú'), 
('Textil del Valle'); 

-- Insertar datos en la tabla 'productos'
INSERT INTO productos (descripcion, sku, marca_id, proveedor_id, supervisor_id, division, estado, oh_disponible, nuevo_oh) VALUES
-- Abarrotes y bebidas
('Aceite Vegetal Primor 1L', 'ACEI0001', (SELECT id FROM marcas WHERE nombre = 'Alicorp'), (SELECT id FROM proveedores WHERE nombre = 'Agrokasa'), 2, 'Abarrotes', TRUE, 500, 100),
('Cerveza Cristal Lata 355ml', 'CERV0001', (SELECT id FROM marcas WHERE nombre = 'Backus y Johnston'), (SELECT id FROM proveedores WHERE nombre = 'Marex'), 2, 'Bebidas', TRUE, 1200, 200),
('Gaseosa Inca Kola Botella 1.5L', 'GASE0001', (SELECT id FROM marcas WHERE nombre = 'Inca Kola'), (SELECT id FROM proveedores WHERE nombre = 'Agrokasa'), 2, 'Bebidas', TRUE, 800, 150),

-- Congelados y lácteos
('Helado Sublime Chocolate', 'HELA0001', (SELECT id FROM marcas WHERE nombre = 'Donofrio'), (SELECT id FROM proveedores WHERE nombre = 'Frozen Products Corporation'), 2, 'Congelados', TRUE, 300, 50),
('Leche Fresca UHT Laive 1L', 'LECH0001', (SELECT id FROM marcas WHERE nombre = 'Laive'), (SELECT id FROM proveedores WHERE nombre = 'DanPer'), 2, 'Lácteos', TRUE, 700, 100),

-- Textiles
('Chalina de Baby Alpaca', 'TEXT0001', (SELECT id FROM marcas WHERE nombre = 'Sol Alpaca'), (SELECT id FROM proveedores WHERE nombre = 'Michell & Co.'), 2, 'Textiles', TRUE, 150, 30),
('Polo Algodón Pima', 'TEXT0002', (SELECT id FROM marcas WHERE nombre = 'Dunkelvolk'), (SELECT id FROM proveedores WHERE nombre = 'Kusa Cotton Peru'), 2, 'Textiles', TRUE, 400, 80),

-- Condimentos y frutas
('Ají Amarillo Pasta 200g', 'ALIM0001', (SELECT id FROM marcas WHERE nombre = 'Incas Food'), (SELECT id FROM proveedores WHERE nombre = 'Peimco'), 2, 'Condimentos', TRUE, 250, 40),
('Palta Hass Exportación Caja 4kg', 'FRUT0001', (SELECT id FROM marcas WHERE nombre = 'Camposol'), (SELECT id FROM proveedores WHERE nombre = 'Agrokasa'), 2, 'Frutas Frescas', TRUE, 600, 120),

-- Minería y pescados
('Concentrado de Cobre', 'MINA0001', (SELECT id FROM marcas WHERE nombre = 'Cerro Verde'), (SELECT id FROM proveedores WHERE nombre = 'Antamina'), 2, 'Minería', TRUE, 100, 20),
('Filete de Jurel Congelado 1kg', 'PESC0001', (SELECT id FROM marcas WHERE nombre = 'Campomar'), (SELECT id FROM proveedores WHERE nombre = 'Frozen Products Corporation'), 2, 'Pescados Congelados', TRUE, 200, 50),

-- Otros rubros
('Artesanía Cerámica Retablo', 'ARTE0001', (SELECT id FROM marcas WHERE nombre = 'Ajegroup'), (SELECT id FROM proveedores WHERE nombre = 'Berrocal'), 2, 'Artesanía', TRUE, 50, 10),
('Yogur Natural Gloria 1kg', 'YOGU0001', (SELECT id FROM marcas WHERE nombre = 'Gloria'), (SELECT id FROM proveedores WHERE nombre = 'Marex'), 2, 'Lácteos', TRUE, 450, 80),
('Bebida Energizante Sporade 500ml', 'BEBE0001', (SELECT id FROM marcas WHERE nombre = 'Ajegroup'), (SELECT id FROM proveedores WHERE nombre = 'DanPer'), 2, 'Bebidas', TRUE, 600, 100),
('Suéter de Alpaca Alta Calidad', 'TEXT0003', (SELECT id FROM marcas WHERE nombre = 'Kuna'), (SELECT id FROM proveedores WHERE nombre = 'Michell & Co.'), 2, 'Textiles', TRUE, 80, 15),
('Espárragos Verdes Frescos 500g', 'VEGE0001', (SELECT id FROM marcas WHERE nombre = 'Gloria'), (SELECT id FROM proveedores WHERE nombre = 'DanPer'), 2, 'Vegetales Frescos', TRUE, 350, 70),
('Arándanos Frescos Bandeja 250g', 'FRUT0002', (SELECT id FROM marcas WHERE nombre = 'Gloria'), (SELECT id FROM proveedores WHERE nombre = 'Hortifrut Perú'), 2, 'Frutas Frescas', TRUE, 400, 90),
('Tela de Algodón Pima por metro', 'TEXT0004', (SELECT id FROM marcas WHERE nombre = 'Kuna'), (SELECT id FROM proveedores WHERE nombre = 'Textil del Valle'), 2, 'Materias Primas Textiles', TRUE, 1000, 200);

INSERT INTO pedidos (supervisor_id, producto_id, cantidad, fecha) VALUES
(2, 1, 25, '2025-06-30 08:30:00'),   -- Aceite Vegetal Primor
(4, 2, 40, '2025-06-30 09:15:00'),   -- Cerveza Cristal
(2, 3, 30, '2025-06-30 10:45:00'),   -- Inca Kola
(4, 4, 20, '2025-06-30 13:00:00'),   -- Helado Sublime
(2, 5, 35, '2025-06-30 15:10:00'),   -- Leche Laive
(4, 6, 18, '2025-06-30 17:25:00'),   -- Chalina Baby Alpaca
(2, 7, 50, '2025-07-01 08:20:00'),   -- Polo Pima
(4, 8, 45, '2025-07-01 09:50:00'),   -- Ají Amarillo
(2, 9, 60, '2025-07-01 11:00:00'),   -- Palta Hass
(4, 10, 55, '2025-07-01 13:30:00'),  -- Concentrado de Cobre
(2, 11, 22, '2025-07-01 14:45:00'),  -- Filete de Jurel
(4, 12, 33, '2025-07-01 16:00:00'),  -- Retablo
(2, 13, 70, '2025-07-01 18:15:00'),  -- Yogur Gloria
(4, 14, 48, '2025-07-02 09:10:00'),  -- Sporade
(2, 15, 65, '2025-07-02 11:00:00'),  -- Suéter de Alpaca
(4, 16, 28, '2025-07-02 13:25:00'),  -- Espárragos
(2, 17, 90, '2025-07-02 15:15:00'),  -- Arándanos
(4, 18, 42, '2025-07-02 17:05:00');  -- Tela de Algodón

select * from pedidos
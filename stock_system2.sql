-- Database: stock_system

-- DROP DATABASE IF EXISTS stock_system;

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

CREATE TABLE marcas (
    id SERIAL PRIMARY KEY
);

CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY
);

ALTER TABLE productos
ADD COLUMN proveedor_id INTEGER,
ADD CONSTRAINT fk_proveedor FOREIGN KEY (proveedor_id) REFERENCES proveedores(id);

ALTER TABLE marcas ADD COLUMN nombre VARCHAR(100) UNIQUE NOT NULL;
ALTER TABLE proveedores ADD COLUMN nombre VARCHAR(100) UNIQUE NOT NULL;

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    sku CHAR(8) UNIQUE NOT NULL,
    marca_id INT,
    proveedor VARCHAR(100),
    division VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,
    oh_disponible INTEGER DEFAULT 0,
    nuevo_oh INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_marca FOREIGN KEY (marca_id) REFERENCES marcas(id) ON DELETE SET NULL
);

select * from proveedores
select * from marcas
select * from productos
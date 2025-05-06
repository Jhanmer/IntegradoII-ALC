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

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    sku VARCHAR(100),
    marca VARCHAR(100),
    proveedor VARCHAR(100),
    division VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,  -- TRUE = Activo, FALSE = Inactivo
    oh_disponible INTEGER DEFAULT 0,
    nuevo_oh INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM PRODUCTOS

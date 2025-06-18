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

-- Tabla de productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    sku CHAR(8) UNIQUE NOT NULL,
    marca_id INT,
    proveedor_id INT,
    division VARCHAR(100),  -- division como texto
    estado BOOLEAN DEFAULT TRUE,
    oh_disponible INTEGER DEFAULT 0,
    nuevo_oh INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_marca FOREIGN KEY (marca_id) REFERENCES marcas(id) ON DELETE SET NULL,
    CONSTRAINT fk_proveedor FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE SET NULL
);

select * from proveedores
select * from marcas
select * from productos

CREATE TABLE usuario (
    CodUsu SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    login VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo'
);

INSERT INTO usuario (nombre, rol, login, password, estado) VALUES
('Juan Perez', 'administrador', 'juan@alicorp.pe', 'hash_password_admin', 'activo'),
('Maria Lopez', 'supervisor', 'maria@alicorp.pe', 'hash_password_supervisor', 'activo'),
('Carlos Garcia', 'mercader', 'carlos@alicorp.pe', 'hash_password_mercader', 'activo'),
('Ana Rodriguez', 'supervisor', 'ana@alicorp.pe', 'hash_password_supervisor', 'activo');


select * from usuario;
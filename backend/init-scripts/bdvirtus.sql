-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS bdvirtus;

-- Usar la base de datos existente
USE bdvirtus;

-- Eliminar las tablas si ya existen
DROP TABLE IF EXISTS InvestigadorProducto;
DROP TABLE IF EXISTS Producto;
DROP TABLE IF EXISTS Investigador;
DROP TABLE IF EXISTS TipoDeProducto;

-- Crear tabla de Tipos de Producto
CREATE TABLE TipoDeProducto (
    idTipoDeProducto INT AUTO_INCREMENT PRIMARY KEY,
    nombreTipoDeProducto VARCHAR(100) NOT NULL
);

-- Crear tabla de Productos (después de TipoDeProducto)
CREATE TABLE Producto (
    idProducto INT AUTO_INCREMENT PRIMARY KEY,
    TituloProducto VARCHAR(255) NOT NULL,
    linkVisualizacion VARCHAR(500),
    codigoUnico VARCHAR(50) UNIQUE NOT NULL,
    ano INT NOT NULL,  -- Usar INT en lugar de YEAR si el error persiste
    idTipoDeProducto INT NOT NULL,
    FOREIGN KEY (idTipoDeProducto) REFERENCES TipoDeProducto(idTipoDeProducto)
);

-- Crear tabla de Investigadores
CREATE TABLE Investigador (
    idInvestigador INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL
);

-- Crear tabla intermedia para la relación de muchos a muchos
CREATE TABLE InvestigadorProducto (
    idInvestigador INT NOT NULL,
    idProducto INT NOT NULL,
    PRIMARY KEY (idInvestigador, idProducto),
    FOREIGN KEY (idInvestigador) REFERENCES Investigador(idInvestigador),
    FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
);

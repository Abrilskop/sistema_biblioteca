-- =========================================================
-- SCRIPT COMPLETO PARA LA BASE DE DATOS 'bdserviciobiblioteca'
-- =========================================================

-- 1. CREACIÓN DE LA BASE DE DATOS
CREATE DATABASE IF NOT EXISTS `bdserviciobiblioteca`;
USE `bdserviciobiblioteca`;

-- 2. ELIMINACIÓN DE TABLAS (en orden inverso a la creación para evitar errores de claves foráneas)
DROP TABLE IF EXISTS `prestamo`;
DROP TABLE IF EXISTS `ejemplar`;
DROP TABLE IF EXISTS `solicitante`;
DROP TABLE IF EXISTS `libro`;

-- 3. CREACIÓN DE TABLAS
CREATE TABLE `libro` (
  `ISBN` varchar(17) NOT NULL,
  `Titulo` varchar(255) NOT NULL,
  `Autor` varchar(255) NOT NULL,
  `Anio_Publicacion` year DEFAULT NULL,
  PRIMARY KEY (`ISBN`)
) ENGINE=InnoDB;

CREATE TABLE `solicitante` (
  `ID_Solicitante` int NOT NULL AUTO_INCREMENT,
  `cdni` varchar(10) NOT NULL,
  `Nombre` varchar(60) NOT NULL,
  `Paterno` varchar(60) NOT NULL,
  `Materno` varchar(60) NOT NULL,
  `Tipo_Usuario` enum('Estudiante','Profesor','Administrativo') NOT NULL,
  `Activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`ID_Solicitante`)
) ENGINE=InnoDB;

CREATE TABLE `ejemplar` (
  `ID_Ejemplar` varchar(50) NOT NULL,
  `ISBN` varchar(17) NOT NULL,
  `Estado` enum('Disponible','Prestado','En Reparacion','Extraviado') NOT NULL DEFAULT 'Disponible',
  PRIMARY KEY (`ID_Ejemplar`),
  KEY `ISBN` (`ISBN`),
  CONSTRAINT `ejemplar_ibfk_1` FOREIGN KEY (`ISBN`) REFERENCES `libro` (`ISBN`)
) ENGINE=InnoDB;

CREATE TABLE `prestamo` (
  `ID_Prestamo` int NOT NULL AUTO_INCREMENT,
  `ID_Ejemplar` varchar(50) NOT NULL,
  `ID_Solicitante` int NOT NULL,
  `Fecha_Prestamo` date NOT NULL,
  `Fecha_Devolucion_Prevista` date NOT NULL,
  `Fecha_Devolucion_Real` date DEFAULT NULL,
  PRIMARY KEY (`ID_Prestamo`),
  KEY `ID_Ejemplar` (`ID_Ejemplar`),
  KEY `ID_Solicitante` (`ID_Solicitante`),
  CONSTRAINT `prestamo_ibfk_1` FOREIGN KEY (`ID_Ejemplar`) REFERENCES `ejemplar` (`ID_Ejemplar`),
  CONSTRAINT `prestamo_ibfk_2` FOREIGN KEY (`ID_Solicitante`) REFERENCES `solicitante` (`ID_Solicitante`)
) ENGINE=InnoDB;


-- 4. CREACIÓN DE PROCEDIMIENTOS ALMACENADOS
DELIMITER $$

-- PROCEDIMIENTOS DE MANTENIMIENTO
DROP PROCEDURE IF EXISTS sp_registrar_libro $$
CREATE PROCEDURE sp_registrar_libro(IN pISBN VARCHAR(17), IN pTitulo VARCHAR(255), IN pAutor VARCHAR(255), IN pAnio_Publicacion YEAR)
BEGIN
    INSERT INTO libro(ISBN, Titulo, Autor, Anio_Publicacion) VALUES (pISBN, pTitulo, pAutor, pAnio_Publicacion);
END $$

DROP PROCEDURE IF EXISTS sp_registrar_ejemplar $$
CREATE PROCEDURE sp_registrar_ejemplar(IN pID_Ejemplar VARCHAR(50), IN pISBN VARCHAR(17))
BEGIN
    INSERT INTO ejemplar (ID_Ejemplar, ISBN, Estado) VALUES (pID_Ejemplar, pISBN, 'Disponible');
END $$

DROP PROCEDURE IF EXISTS sp_cambiar_estado_ejemplar $$
CREATE PROCEDURE sp_cambiar_estado_ejemplar(IN pID_Ejemplar VARCHAR(50), IN pEstado ENUM('Disponible','Prestado','En Reparacion','Extraviado'))
BEGIN
    UPDATE ejemplar SET Estado = pEstado WHERE ID_Ejemplar = pID_Ejemplar;
END $$

DROP PROCEDURE IF EXISTS sp_registrar_prestamo $$
CREATE PROCEDURE sp_registrar_prestamo(IN pID_Ejemplar VARCHAR(50), IN pID_Solicitante INT, IN pFecha_Prestamo DATE, IN pFecha_Devolucion_Prevista DATE, OUT pID_Prestamo INT)
BEGIN
    START TRANSACTION;
        INSERT INTO prestamo (ID_Ejemplar, ID_Solicitante, Fecha_Prestamo, Fecha_Devolucion_Prevista)
        VALUES (pID_Ejemplar, pID_Solicitante, pFecha_Prestamo, pFecha_Devolucion_Prevista);
        SET pID_Prestamo = LAST_INSERT_ID();
        UPDATE ejemplar SET Estado = 'Prestado' WHERE ID_Ejemplar = pID_Ejemplar;
    COMMIT;
END $$

DROP PROCEDURE IF EXISTS sp_devolver_prestamo $$
CREATE PROCEDURE sp_devolver_prestamo(IN pID_Prestamo INT, IN pFecha_Devolucion_Real DATE)
BEGIN
    DECLARE vID_Ejemplar VARCHAR(50);
    SELECT ID_Ejemplar INTO vID_Ejemplar FROM prestamo WHERE ID_Prestamo = pID_Prestamo;
    START TRANSACTION;
        UPDATE prestamo SET Fecha_Devolucion_Real = pFecha_Devolucion_Real WHERE ID_Prestamo = pID_Prestamo;
        UPDATE ejemplar SET Estado = 'Disponible' WHERE ID_Ejemplar = vID_Ejemplar;
    COMMIT;
END $$

-- PROCEDIMIENTOS DE LISTADO (LOS QUE FALTABAN)
DROP PROCEDURE IF EXISTS sp_listar_libros $$
CREATE PROCEDURE sp_listar_libros()
BEGIN
    SELECT ISBN, Titulo FROM libro ORDER BY Titulo;
END$$

DROP PROCEDURE IF EXISTS sp_listar_ejemplares $$
CREATE PROCEDURE sp_listar_ejemplares()
BEGIN
    SELECT e.ID_Ejemplar, e.ISBN, l.Titulo, e.Estado
      FROM ejemplar e JOIN libro l ON e.ISBN = l.ISBN
     ORDER BY e.ID_Ejemplar;
END$$

DROP PROCEDURE IF EXISTS sp_listar_solicitantes_activos $$
CREATE PROCEDURE sp_listar_solicitantes_activos()
BEGIN
    SELECT ID_Solicitante, Nombre, Paterno, Materno
      FROM solicitante WHERE Activo = 1
     ORDER BY Paterno, Materno, Nombre;
END$$

DROP PROCEDURE IF EXISTS sp_listar_prestamos $$
CREATE PROCEDURE sp_listar_prestamos(IN pSoloPendientes TINYINT)
BEGIN
    SELECT p.ID_Prestamo, p.ID_Ejemplar, e.Estado, s.ID_Solicitante, s.Nombre, s.Paterno, s.Materno,
           p.Fecha_Prestamo, p.Fecha_Devolucion_Prevista, p.Fecha_Devolucion_Real
      FROM prestamo p
      JOIN solicitante s ON s.ID_Solicitante = p.ID_Solicitante
      JOIN ejemplar e ON e.ID_Ejemplar = p.ID_Ejemplar
     WHERE (pSoloPendientes = 1 AND p.Fecha_Devolucion_Real IS NULL) OR pSoloPendientes = 0
     ORDER BY p.Fecha_Prestamo DESC;
END$$

DELIMITER ;

-- 5. INSERCIÓN DE DATOS DE PRUEBA
INSERT INTO `libro` VALUES 
('978-0132350884','Clean Code','Robert C. Martin',2008),
('978-0201633610','Design Patterns','Erich Gamma',1994),
('978-0596007126','Python Cookbook','Alex Martelli',2005);

INSERT INTO `solicitante` (cdni, Nombre, Paterno, Materno, Tipo_Usuario, Activo) VALUES 
('12345678','Juan','Perez','Gomez','Estudiante',1),
('87654321','Maria','Lopez','Diaz','Profesor',1),
('11223344','Pedro','Martinez','Sanchez','Estudiante',0);

INSERT INTO `ejemplar` VALUES 
('EJ-0001','978-0132350884','Disponible'),
('EJ-0002','978-0132350884','Disponible'),
('EJ-0003','978-0201633610','En Reparacion'),
('EJ-0004','978-0596007126','Extraviado');
-- *************************************************************************
-- ** CÓDIGO PARA ABRIR EL ACCESO REMOTO AL USUARIO 'root' **
-- ** Se ejecuta en la MÁQUINA A (Servidor de Base de Datos) **
-- *************************************************************************

USE mysql;

-- 1. Si el usuario 'root'@'%' ya existe (por el intento anterior), lo eliminamos para evitar conflictos
DROP USER IF EXISTS 'root'@'%';

-- 2. Creamos el usuario 'root' con acceso desde cualquier host ('%')
--    Asegúrate de reemplazar 'tu_contraseña_root' con la contraseña real del usuario root
CREATE USER 'root'@'%' IDENTIFIED BY 'REEMPLAZA_POR_TU_CONTRASEÑA'; 

-- 3. Concedemos TODOS los privilegios sobre TODAS las bases de datos (representado por *.*)
--    ESTA ES LA SINTAXIS CORREGIDA:
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION; 

-- 4. Actualizar las tablas de privilegios para que los cambios surtan efecto de inmediato
FLUSH PRIVILEGES;

-- 5. Opcional: Verificar que el usuario 'root'@'%' ha sido creado
SELECT User, Host FROM mysql.user WHERE User = 'root' AND Host = '%';

-- NOTA: Si utilizaste otro usuario diferente a 'root' para tu aplicación, 
-- reemplaza 'root' por ese nombre de usuario.
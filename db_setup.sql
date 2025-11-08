-- ================================================
--  Script oficial de inicialización de base de datos NUAM
-- ================================================

-- 1. Crear Base de Datos
CREATE DATABASE IF NOT EXISTS nuam CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. Crear Usuario (si no existe)
CREATE USER IF NOT EXISTS 'nuamuser'@'localhost' IDENTIFIED BY 'NuamPass123';

-- 3. Otorgar permisos al usuario
GRANT ALL PRIVILEGES ON nuam.* TO 'nuamuser'@'localhost';

-- 4. Aplicar cambios
FLUSH PRIVILEGES;

-- 5. Seleccionar base de datos
USE nuam;

-- (Opcional) puedes agregar tablas manuales aquí si algún día lo necesitas.

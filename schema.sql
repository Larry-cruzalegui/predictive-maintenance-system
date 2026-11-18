-- Crear la base de datos para el mantenimiento industrial
CREATE DATABASE IF NOT EXISTS MantenimientoIndustrialDB;
USE MantenimientoIndustrialDB;

-- Crear la tabla de registros de los sensores de las máquinas
CREATE TABLE IF NOT EXISTS sensores_maquinas (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_maquina VARCHAR(50) NOT NULL,
    temperatura_c FLOAT NOT NULL,
    vibracion_mm_s FLOAT NOT NULL,
    horas_operacion INT NOT NULL,
    mantenimiento_reciente INT NOT NULL, -- 0 = No, 1 = Sí
    fallo_inminente INT NOT NULL        -- 0 = Operando bien, 1 = Fallo detectado
);

-- Insertar datos de prueba iniciales para simular registros históricos
INSERT INTO sensores_maquinas (id_maquina, temperatura_c, vibracion_mm_s, horas_operacion, mantenimiento_reciente, fallo_inminente) VALUES
('MAQ-001', 75.5, 2.1, 1200, 0, 0),
('MAQ-002', 98.2, 5.8, 4500, 1, 1),
('MAQ-003', 68.0, 1.5, 800, 0, 0),
('MAQ-004', 102.4, 6.3, 5000, 0, 1),
('MAQ-005', 72.1, 1.8, 1100, 1, 0);

-- Consulta de prueba para extraer los datos que procesaremos en Python
SELECT temperatura_c, vibracion_mm_s, horas_operacion, mantenimiento_reciente, fallo_inminente 
FROM sensores_maquinas;
USE healthcare_system_db;

-- 1. Modificamos la columna id_supplier para asegurarnos de que acepte campos vacíos (NULL)
-- (Quitamos cualquier restricción 'NOT NULL' que pudiera trabar el Data Entry web)
ALTER TABLE equipment MODIFY COLUMN id_supplier INT NULL;

-- 2. Inyectamos las columnas exigidas por la Tabla 1 del manual técnico de la OMS
-- (Requerimientos de energía y una estampa de tiempo que se actualiza sola al modificar datos)
ALTER TABLE equipment 
ADD COLUMN power_requirements VARCHAR(100) DEFAULT '220V / Batería interna' AFTER location,
ADD COLUMN date_inventory_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER id_supplier;

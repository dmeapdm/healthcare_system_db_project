-- =========================================================================
-- 06: CONSUMO DE INVENTARIO DUAL - MOTIVO DE REPOSICIÓN OBLIGATORIO
-- Bloque 1: catálogo de motivos + enforcement a nivel de motor SQL
-- para egresos directos (sin orden de trabajo).
-- =========================================================================
-- Requisito previo: haber corrido 05_inputs_stock_movements_upgrade.sql
-- (crea la tabla stock_movements que este script modifica).
-- Este script NO borra ni modifica datos existentes en stock_movements.
-- =========================================================================

USE healthcare_system_db;

-- 1. Tabla catálogo de motivos de reposición
CREATE TABLE IF NOT EXISTS reposition_reasons (
    id_reason INT AUTO_INCREMENT PRIMARY KEY,
    reason_name VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO reposition_reasons (reason_name) VALUES
    ('Reposición por rotura'),
    ('Préstamo a servicio'),
    ('Vencimiento'),
    ('Reposición rápida'),
    ('Ajuste por control físico de stock'),
    ('Otro (detallar en observaciones)');

-- 2. Columna id_reason en stock_movements
-- Se agrega como NULL primero para no romper filas ya existentes en la tabla;
-- la obligatoriedad real para egresos directos se aplica en el paso 4.
ALTER TABLE stock_movements
    ADD COLUMN id_reason INT NULL AFTER movement_type;

-- 3. Foreign key hacia el catálogo
ALTER TABLE stock_movements
    ADD CONSTRAINT fk_stock_movement_reason
    FOREIGN KEY (id_reason) REFERENCES reposition_reasons(id_reason)
    ON DELETE RESTRICT;

-- 4. CHECK constraint: bloquea a nivel de motor cualquier INSERT/UPDATE de tipo
--    'salida_directa' que no traiga id_reason. Los demás movement_type
--    (salida_orden, ingreso_compra, ajuste_inventario) no se ven forzados,
--    porque el motivo de reposición solo aplica al egreso directo sin OT.
--    Requiere MySQL 8.0.16+ (los CHECK ya se evalúan, no solo se parsean).
ALTER TABLE stock_movements
    ADD CONSTRAINT chk_direct_exit_requires_reason
    CHECK (movement_type <> 'salida_directa' OR id_reason IS NOT NULL);

-- Verificación
SELECT * FROM reposition_reasons;
DESCRIBE stock_movements;
-- =========================================================================
-- 05: UNIFICACIÓN DE ALMACÉN (insumos + repuestos + herramientas)
-- Y BITÁCORA GENERAL DE MOVIMIENTOS DE STOCK (con o sin orden de trabajo)
-- =========================================================================
-- ⚠️ ADVERTENCIA: Este script BORRA la tabla "inputs" actual y la vuelve a
-- crear. Si ya cargaste datos reales en ella, hacé un respaldo antes:
--   mysqldump -u root -p healthcare_system_db inputs > backup_inputs.sql
-- =========================================================================

USE healthcare_system_db;

-- 1. Eliminamos las tablas dependientes en el orden correcto (por las FK)
DROP TABLE IF EXISTS stock_movements;
DROP TABLE IF EXISTS work_order_inputs;
DROP TABLE IF EXISTS inputs;

-- 2. Tabla unificada de almacén: insumos clínicos, insumos de taller,
--    repuestos técnicos y herramientas, todo en un solo lugar.
CREATE TABLE inputs (
    id_inputs INT AUTO_INCREMENT PRIMARY KEY,
    internal_code VARCHAR(50) UNIQUE,                 -- tu código interno (ej. el "INSUMO SI2" del Excel)
    input_type VARCHAR(30) NOT NULL CHECK (input_type IN (
        'insumo_clinico',      -- se despacha a servicios (UCI, Guardia, Neonatología...)
        'insumo_taller',       -- uso interno de electromedicina
        'repuesto_tecnico',    -- ligado a reparaciones de equipos
        'herramienta'          -- instrumental de taller
    )),
    input_category VARCHAR(100),                       -- 'PRESION ARTERIAL', 'SATUROMETRIA', 'FERRETERIA'...
    brand VARCHAR(100) DEFAULT 'GENERICO',
    model_ref VARCHAR(100),
    name_input TEXT NOT NULL,
    unit_of_measure VARCHAR(20) NOT NULL DEFAULT 'unidad',
    cabinet_space VARCHAR(100),
    drawer_location VARCHAR(100),
    stock INT NOT NULL DEFAULT 0,
    min_stock_alert INT NOT NULL DEFAULT 5,
    unit_price DECIMAL(10,2),
    id_supplier INT,                                    -- FK real a supplier (no texto libre)
    compatible_equipment VARCHAR(150),                  -- solo repuestos: a qué equipo/modelo corresponde
    procurement_notes VARCHAR(255),                     -- notas de gestión de compra en curso
    is_active BOOLEAN DEFAULT TRUE,                      -- para dar de baja sin borrar historial

    FOREIGN KEY (id_supplier) REFERENCES supplier(id_supplier) ON DELETE SET NULL
);

-- 3. Tabla intermedia clásica (se mantiene por compatibilidad con el flujo
--    de "consumo dentro de una orden de trabajo" ya armado)
CREATE TABLE work_order_inputs (
    id_work_order INT NOT NULL,
    id_inputs INT NOT NULL,
    quantity_used INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_work_order, id_inputs),
    FOREIGN KEY (id_work_order) REFERENCES work_order(id_work_order) ON DELETE RESTRICT,
    FOREIGN KEY (id_inputs) REFERENCES inputs(id_inputs) ON DELETE RESTRICT
);

-- 4. Bitácora general: registra TODO movimiento de stock, tenga o no
--    una orden de trabajo asociada (cubre despachos directos a UCI,
--    Guardia, Neonatología, etc. sin necesidad de abrir una orden).
CREATE TABLE stock_movements (
    id_movement INT AUTO_INCREMENT PRIMARY KEY,
    id_inputs INT NOT NULL,
    id_work_order INT NULL,                             -- NULL = despacho directo sin orden
    movement_type VARCHAR(20) NOT NULL CHECK (movement_type IN (
        'salida_orden',        -- consumido en una reparación
        'salida_directa',      -- despachado a un servicio sin orden
        'ingreso_compra',      -- entra stock nuevo
        'ajuste_inventario'    -- corrección manual (conteo físico, pérdida, etc.)
    )),
    quantity INT NOT NULL,
    destination_service VARCHAR(100),
    requested_by VARCHAR(100),
    dispatched_by VARCHAR(100),
    movement_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,

    FOREIGN KEY (id_inputs) REFERENCES inputs(id_inputs) ON DELETE RESTRICT,
    FOREIGN KEY (id_work_order) REFERENCES work_order(id_work_order) ON DELETE SET NULL
);

-- Queries de verificación
SELECT * FROM inputs;
SELECT * FROM work_order_inputs;
SELECT * FROM stock_movements;
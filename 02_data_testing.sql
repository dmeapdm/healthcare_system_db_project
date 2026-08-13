USE healthcare_system_db;
-- To testing we have to charge data suppliers and inputs as examples. 
-- First: data suppliers
INSERT INTO supplier (name_supplier, email, phone, technical_support, phone_technical_support, email_technical_support) 
VALUES 
('BioMedica Comahue', 'soporte@biomedicacomahue.com.ar', '299-4445566', 'Ing. Christian Gómez', '299-154112233', 'cgomez@biomedicacomahue.com.ar'),
('Gases Medicos del Sur', 'ventas@gasesdelsur.com', '299-4433221', 'Tec. Walter Rogers', '299-155998877', 'guardia@gasesdelsur.com');

-- Second: data inputs
INSERT INTO inputs (code_input, name_input, location, stock, min_stock_alert)
VALUES
('BAT-12V-2A', 'Bateria Plomo-Acido 12V 2Ah (Monitores)', 'Estante A - Caja 3', 12, 4),
('FIL-HEPA-VENT', 'Filtro HEPA para Ventilador Mecanico', 'Estante B - Armario Azul', 3, 5), -- Este nace con stock bajo
('OXY-VAL-01', 'O-Ring de silicona para valvula de Oxigeno', 'Cajonera Tecnica - Nivel 1', 50, 10);

-- Third: data equipment
-- Insertamos un Monitor de Signos Vitales vinculado al proveedor ID 1 (BioMedica Comahue)
INSERT INTO equipment (serial_number_factory, type_device, category, brand, model, year_manufactured, state, location, id_supplier)
VALUES ('SN-MIND-9982', 'Monitor de Signos Vitales', 'Soporte de Vida', 'Mindray', 'UMEC 12', 2022, 'OK', 'Quirofano 1', 1);

-- Insertamos un Panel de Oxígeno Central vinculado al proveedor ID 2 (Gases Medicos del Sur)
INSERT INTO equipment (serial_number_factory, type_device, category, brand, model, year_manufactured, state, location, id_supplier)
VALUES ('SN-MESS-0041', 'Panel de Oxigeno Central', 'Gases Medicos', 'Messer', 'Oxymed 200', 2019, 'OK', 'Terapia Intensiva - Cama 4', 2);

-- Testing "fatal error" in the table equipment and verify: state VARCHAR(50) CHECK (state IN ('OK', 'MAINTENANCE', 'OUT_OF_SERVICE', 'DISPOSED')) DEFAULT 'OK',
INSERT INTO equipment (serial_number_factory, type_device, category, brand, model, state, id_supplier)
VALUES ('SN-ERROR-1', 'Bomba de Infusion', 'Bomba', 'B.Braun', 'Infusomat', 'ROTO_Y_DESARMADO', 1);

-- Testing "fatal error" in the table equipment and verify: FOREIGN KEY (id_supplier) REFERENCES supplier(id_supplier) ON DELETE SET NULL
INSERT INTO equipment (serial_number_factory, type_device, category, brand, model, state, id_supplier)
VALUES ('SN-ERROR-2', 'Electrocardiografo', 'Cardiologia', 'Fukuda', 'FX-8222', 'OK', 99);

-- Testing open and close work_order
-- A) Abrimos y cerramos la Orden de Trabajo para el Monitor Mindray (ID 1)
INSERT INTO work_order (id_equipment, date_work_start, date_work_finish, type_maintenance, description_fault, description_work_done, technical_responsible)
VALUES (1, '2026-08-07 08:30:00', '2026-08-07 10:15:00', 'corrective', 'El monitor se apaga inmediatamente al desconectar de la red eléctrica de 220V.', 'Se constata batería interna agotada y sulfatada. Se realiza el reemplazo por un repuesto nuevo de stock.', 'TuNombreApellido');

-- B) Usamos la TABLA INTERMEDIA: Registramos que en la Orden #1 se gastó 1 unidad del Insumo ID 1 (Batería)
INSERT INTO work_order_inputs (id_work_order, id_inputs, quantity_used)
VALUES (1, 1, 1);

-- Restamos 1 unidad al insumo ID 1 (Batería) porque la gastamos en la reparación
UPDATE inputs 
SET stock = stock - 1 
WHERE id_inputs = 1;





SELECT * FROM supplier;
SELECT * FROM inputs;
SELECT * FROM equipment;
SELECT * FROM work_order;
SELECT * FROM  work_order_inputs;



SELECT 
    w.id_work_order AS 'N° Orden',
    e.brand AS 'Marca',
    e.model AS 'Modelo',
    w.type_maintenance AS 'Tipo',
    w.description_work_done AS 'Trabajo Realizado',
    i.name_input AS 'Insumo Cambiado',
    wi.quantity_used AS 'Cantidad Gastada'
FROM work_order w
JOIN equipment e ON w.id_equipment = e.id_equipment
JOIN work_order_inputs wi ON w.id_work_order = wi.id_work_order
JOIN inputs i ON wi.id_inputs = i.id_inputs;

-- ===============================================================
-- CALCULATE DOWNTIME OF EQUIPMENT APROACH
-- ===============================================================
SELECT 
    w.id_work_order AS 'N° Orden',
    w.id_equipment AS 'ID Equipo',
    
	TIMESTAMPDIFF(MINUTE, w.date_work_start, w.date_work_finish) AS 'Minutos Fuera de Servicio',
    -- AQUÍ RELLENA LA FUNCIÓN PARA CALCULAR EN HORAS:
	TIMESTAMPDIFF(HOUR, w.date_work_start, w.date_work_finish) AS 'Horas Fuera de Servicio'

FROM work_order w;


-- ===============================================================
-- CALCULATE DOWNTIME OF EQUIPMENT ENHANCED
-- ===============================================================

SELECT 
    w.id_work_order AS 'N° Orden',
    w.id_equipment AS 'ID Equipo',
    CONCAT(
        (TIMESTAMPDIFF(MINUTE, w.date_work_start, w.date_work_finish) DIV 60), ' horas y ',
        (TIMESTAMPDIFF(MINUTE, w.date_work_start, w.date_work_finish) % 60), ' minutos'
    ) AS 'Tiempo Fuera de Servicio Real' -- <-- Fíjate que arriba de esta línea cerramos el CONCAT
FROM work_order w;



-- ================================================================
-- CALCULATE YEARS OF EQUIPMENT
-- ================================================================
SELECT 
    id_equipment AS 'ID',
    brand AS 'Marca',
    model AS 'Modelo',
    year_manufactured AS 'Año Fab',
    -- AQUÍ RELLENA LA RESTA: (Año Actual automático) MENOS (Año de Fabricación)
    ( YEAR(CURDATE()) - year_manufactured ) AS 'Años de Antigüedad'
FROM equipment;



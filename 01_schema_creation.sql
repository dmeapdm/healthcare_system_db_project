-- 1.- Creation of the database to manage hospital equipments and systems
-- A hospital is a one complexity systems that you can konw. This system have several subsystems and many inputs and outputs
-- One could say the subsystems here are: 
-- * 1.- Biomedical equipment
-- * 2.- Electrical system
-- * 3.- Medical gases
-- * 4.- Water system
-- * 5.- Heating system
-- * 6.- Climatitation system
DROP DATABASE IF EXISTS healthcare_system_db; 
CREATE DATABASE  healthcare_system_db;
USE healthcare_system_db;

-- =========================================================================
-- MODULE: BIOMEDICAL EQUIPMENT MANAGEMENT SYSTEM
-- =========================================================================
-- First we create table supplier, which stores data about equipments supplier
CREATE TABLE supplier (
	id_supplier INT auto_increment PRIMARY KEY, -- Tis number is a identity supplier in db.check
    name_supplier VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    technical_support VARCHAR(100),
    phone_technical_support VARCHAR(50),
    email_technical_support VARCHAR(100)
    );
    
    
-- Second we create table equipment, which stores data about biomedical equipment for management.
-- This table have a relation N-1 because several equipments might be sold for a supplier.     
CREATE TABLE equipment (
	id_equipment INT auto_increment PRIMARY KEY, -- this number will appear in QR code
	serial_number_factory VARCHAR(50) UNIQUE, -- this number is show in each equipment for manufacturer
    type_device VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    model VARCHAR(100),
    year_manufactured INT,
    
     -- CHECK: Solo acepta estados válidos para el hospital en mayúsculas estrictas
    state VARCHAR(50) CHECK (state IN ('OK', 'MAINTENANCE', 'OUT_OF_SERVICE', 'DISPOSED')) DEFAULT 'OK', 
    
    location VARCHAR(100),
    id_supplier INT,
	
    -- Foraign key table equipment
    FOREIGN KEY (id_supplier) REFERENCES supplier(id_supplier) ON DELETE SET NULL
);

-- Thirth we create table inputs. It handles supplies used to  replace equipment parts 
CREATE TABLE inputs (
	id_inputs INT auto_increment PRIMARY KEY,
    code_input VARCHAR(50) UNIQUE NOT NULL,
    name_input VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    stock INT DEFAULT 0,
    
    -- ALERT: Minimum stock level before the laptop workspace flags it for reorder
    min_stock_alert INT DEFAULT 5 
    
);

-- Fourth we create the table Work Order.It tracks maintenance activities on equipment. 
-- This table has an N-1 relation because an equipment might have more than 1 work order over time.
CREATE TABLE work_order (
	id_work_order INT auto_increment PRIMARY KEY, -- this number is the sequence of work done
    id_equipment INT NOT NULL,
    date_work_start DATETIME NOT NULL,
    date_work_finish DATETIME,
    
    -- CHECK: Only accepts 'preventive' or 'corrective' in lowercase to avoid metrics issues
    type_maintenance VARCHAR(50) NOT NULL CHECK (type_maintenance IN ('preventive', 'corrective')), 
    
    description_fault TEXT,
    description_work_done TEXT,
    technical_responsible VARCHAR(100),

	-- Foreign key table work_order (RESTRICT protects history from accidential deletion)
    FOREIGN KEY (id_equipment) REFERENCES equipment(id_equipment) ON DELETE RESTRICT
);


-- Fifth we create an intermediate table between work order and inputs because 
-- we need to know how many inputs were used on which equipment.
CREATE TABLE work_order_inputs (
	id_work_order INT NOT NULL,
    id_inputs INT NOT NULL,
    quantity_used INT NOT NULL DEFAULT 1,
    
    PRIMARY KEY (id_work_order, id_inputs), -- Compound primary key to avoid duplicate items in same order
    
	-- Foraign key table work_order_inputs    
    FOREIGN KEY (id_work_order) REFERENCES work_order(id_work_order) ON DELETE RESTRICT,
    FOREIGN KEY (id_inputs) REFERENCES inputs(id_inputs) ON DELETE RESTRICT
    
);

-- Queries to verify succesfull creation
SELECT * FROM supplier;
SELECT * FROM equipment;
SELECT * FROM inputs;
SELECT * FROM work_order;
SELECT * FROM work_order_inputs;
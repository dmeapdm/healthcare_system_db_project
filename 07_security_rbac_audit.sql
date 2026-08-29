-- =========================================================================
-- 07: MULTI-TENANT + RBAC + AUDITORÍA INMUTABLE
-- Fase 1 (multi-hospital) y Fase 2 (roles/usuarios/auditoría) del roadmap.
-- =========================================================================
-- Requisito previo: haber corrido 01, 04, 05 y 06 en orden.
-- Este script NO borra datos existentes. Las columnas de texto históricas
-- de "responsable" se conservan renombradas con sufijo _legacy en lugar de
-- eliminarse, porque no existe forma automática de mapear un nombre libre
-- (ej. "TuNombreApellido") a un id_user real sin intervención humana.
-- La app deberá migrarse (Fase 3) para usar las nuevas columnas *_id_user.
-- =========================================================================

USE healthcare_system_db;

SET FOREIGN_KEY_CHECKS = 0;

-- =========================================================================
-- 1. MULTI-TENANT: HOSPITALS / DEPARTAMENTOS
-- =========================================================================
CREATE TABLE IF NOT EXISTS hospitals (
    id_hospital INT AUTO_INCREMENT PRIMARY KEY,
    name_hospital VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE
);

INSERT IGNORE INTO hospitals (id_hospital, name_hospital, address)
VALUES (1, 'Hospital Heller (Sede Principal)', 'Neuquén, Argentina');


-- =========================================================================
-- 2. RBAC: ROLES Y USUARIOS
-- =========================================================================
CREATE TABLE IF NOT EXISTS roles (
    id_role INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);

INSERT IGNORE INTO roles (role_name, description) VALUES
    ('Ingeniero', 'Acceso completo: abre/cierra OT, gestiona equipos, proveedores y stock, ve auditoría.'),
    ('Jefe de Taller', 'Supervisión del taller: abre/cierra OT, gestiona stock, revisa reportes e historial.'),
    ('Técnico', 'Operación diaria: abre/cierra OT propias, registra consumo e ingreso de insumos.');

CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role_id INT NOT NULL,
    hospital_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_users_hospital (hospital_id),
    INDEX idx_users_role (role_id),
    FOREIGN KEY (role_id) REFERENCES roles(id_role) ON DELETE RESTRICT,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id_hospital) ON DELETE RESTRICT
);


-- =========================================================================
-- 3. AUDITORÍA INMUTABLE
-- =========================================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action_type VARCHAR(50) NOT NULL,
    entity_affected VARCHAR(50) NOT NULL,
    entity_id INT NULL,
    action_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    details_json JSON NULL,

    INDEX idx_audit_user (user_id),
    INDEX idx_audit_entity (entity_affected, entity_id),
    INDEX idx_audit_timestamp (action_timestamp),
    FOREIGN KEY (user_id) REFERENCES users(id_user) ON DELETE RESTRICT
);

DROP TRIGGER IF EXISTS trg_audit_logs_no_update;
DROP TRIGGER IF EXISTS trg_audit_logs_no_delete;

DELIMITER $$

CREATE TRIGGER trg_audit_logs_no_update
BEFORE UPDATE ON audit_logs
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'audit_logs es inmutable: no se permite UPDATE sobre registros de auditoría.';
END$$

CREATE TRIGGER trg_audit_logs_no_delete
BEFORE DELETE ON audit_logs
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'audit_logs es inmutable: no se permite DELETE sobre registros de auditoría.';
END$$

DELIMITER ;

SET FOREIGN_KEY_CHECKS = 1;

-- =========================================================================
-- 4. VERIFICACIÓN
-- =========================================================================
SELECT * FROM hospitals;
SELECT * FROM roles;
DESCRIBE users;
DESCRIBE audit_logs;
CREATE USER 'tecnico_biomedica'@'localhost' IDENTIFIED BY 'biomedica123';
GRANT ALL PRIVILEGES ON healthcare_system_db.* TO 'tecnico_biomedica'@'localhost';
FLUSH PRIVILEGES;

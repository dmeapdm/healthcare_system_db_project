-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: healthcare_system_db
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `inputs`
--

DROP TABLE IF EXISTS `inputs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inputs` (
  `id_inputs` int NOT NULL AUTO_INCREMENT,
  `internal_code` varchar(50) DEFAULT NULL,
  `input_type` varchar(30) NOT NULL,
  `input_category` varchar(100) DEFAULT NULL,
  `brand` varchar(100) DEFAULT 'GENERICO',
  `model_ref` varchar(100) DEFAULT NULL,
  `name_input` text NOT NULL,
  `unit_of_measure` varchar(20) NOT NULL DEFAULT 'unidad',
  `cabinet_space` varchar(100) DEFAULT NULL,
  `drawer_location` varchar(100) DEFAULT NULL,
  `stock` int NOT NULL DEFAULT '0',
  `min_stock_alert` int NOT NULL DEFAULT '5',
  `unit_price` decimal(10,2) DEFAULT NULL,
  `id_supplier` int DEFAULT NULL,
  `compatible_equipment` varchar(150) DEFAULT NULL,
  `procurement_notes` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_inputs`),
  UNIQUE KEY `internal_code` (`internal_code`),
  KEY `id_supplier` (`id_supplier`),
  CONSTRAINT `inputs_ibfk_1` FOREIGN KEY (`id_supplier`) REFERENCES `supplier` (`id_supplier`) ON DELETE SET NULL,
  CONSTRAINT `inputs_chk_1` CHECK ((`input_type` in (_utf8mb4'insumo_clinico',_utf8mb4'insumo_taller',_utf8mb4'repuesto_tecnico',_utf8mb4'herramienta')))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inputs`
--

LOCK TABLES `inputs` WRITE;
/*!40000 ALTER TABLE `inputs` DISABLE KEYS */;
INSERT INTO `inputs` VALUES (1,'6690','repuesto_tecnico','PRESION ARTERIAL','MINDRAY','CM 1203','MANGUITO NIBP ADULTO 25-35 CM','unidad','GABINETE I','CAJÓN A',4,3,1450.00,NULL,NULL,NULL,1),(2,'12071','insumo_clinico','SATUROMETRÍA','NELLCOR','MAXNI','SENSOR DE OXIMETRIA NEONATAL','unidad','MUEBLE D','D2',4,4,3200.00,NULL,NULL,NULL,1),(6,'2323','repuesto_tecnico','BATERIA','GENERICA','15VAC34','BATERIA','unidad','MUEBLE E','E6',9,5,5000.00,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `inputs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-21 16:50:11

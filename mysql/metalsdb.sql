-- MySQL dump 10.13  Distrib 8.0.28, for Linux (x86_64)
--
-- Host: localhost    Database: metalsdb
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Temporary view structure for view `metalls_v`
--

DROP TABLE IF EXISTS `metalls_v`;
/*!50001 DROP VIEW IF EXISTS `metalls_v`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `metalls_v` AS SELECT 
 1 AS `dt`,
 1 AS `buy`,
 1 AS `sell`,
 1 AS `name`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `metals_codes`
--

DROP TABLE IF EXISTS `metals_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metals_codes` (
  `code` smallint NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metals_codes`
--

LOCK TABLES `metals_codes` WRITE;
/*!40000 ALTER TABLE `metals_codes` DISABLE KEYS */;
INSERT INTO `metals_codes` VALUES (1,'Gold'),(2,'Silver'),(3,'Platina'),(4,'Palladii');
/*!40000 ALTER TABLE `metals_codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metals_data`
--

DROP TABLE IF EXISTS `metals_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metals_data` (
  `dt` date NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `code` smallint NOT NULL,
  `buy` decimal(10,2) NOT NULL,
  `sell` decimal(10,2) NOT NULL,
  UNIQUE KEY `metals_data_UN` (`dt`,`code`),
  KEY `metals_data_id_IDX` (`id`) USING BTREE,
  KEY `metals_data_dc_IDX` (`dt`,`code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=275 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metals_data`
--

LOCK TABLES `metals_data` WRITE;
/*!40000 ALTER TABLE `metals_data` DISABLE KEYS */;
INSERT INTO `metals_data` VALUES ('2022-02-01',267,1,4459.89,4459.89),('2022-02-01',268,2,56.04,56.04),('2022-02-01',269,3,2528.08,2528.08),('2022-02-01',270,4,6022.57,6022.57),('2022-02-02',271,1,4479.74,4479.74),('2022-02-02',272,2,55.78,55.78),('2022-02-02',273,3,2571.54,2571.54),('2022-02-02',274,4,5914.30,5914.30);
/*!40000 ALTER TABLE `metals_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `metalls_v`
--

/*!50001 DROP VIEW IF EXISTS `metalls_v`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`172.17.0.1` SQL SECURITY DEFINER */
/*!50001 VIEW `metalls_v` AS select `md`.`dt` AS `dt`,`md`.`buy` AS `buy`,`md`.`sell` AS `sell`,`mc`.`name` AS `name` from (`metals_codes` `mc` join `metals_data` `md`) where (`mc`.`code` = `md`.`code`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-19 11:21:58

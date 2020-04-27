-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: stock
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES UTF8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author`
--

LOCK TABLES `author` WRITE;
/*!40000 ALTER TABLE `author` DISABLE KEYS */;
INSERT INTO `author` VALUES (1,'egoing','a59b62a99fbd7ef95764938d84da1dda982c47ce6472190f914619a81ebb8e7b'),(2,'duru','4347387e3d00dad3c0243cc440d090e2da18941d3f93974edd064db967b879a5'),(3,'taeho','c26140f0e41bb57687f9c58d4b25875e0c1e4d25f31cf91efb39a0fc9ab7dace'),(4,'sookbu ','82b6fba55af363a284dd6c6bbca588ad6116f08bbd9d3d2b2aa9c1e0815c66c3'),(5,'a','ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb'),(6,'b','3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d'),(7,'c','2e7d2c03a9507ae265ecf5b5356885a53393a2029d241394997265a1a25aefc6'),(8,'d','18ac3e7343f016890c510e93f935261169d9e3f565436429830faf0934f4f8e4'),(9,'e','3f79bb7b435b05321651daefd374cdc681dc06faa65e374e38337b88ca046dea'),(10,'f','252f10c83610ebca1a059c0bae8255eba2f95be4d1d7bcfa89d7248a82d9f111'),(11,'g','cd0aa9856147b6c5b4ff2b7dfee5da20aa38253099ef1b4a64aced233c9afe29');
/*!40000 ALTER TABLE `author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interests`
--

DROP TABLE IF EXISTS `interests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `market_price` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `volume` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `time` datetime NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interests`
--

LOCK TABLES `interests` WRITE;
/*!40000 ALTER TABLE `interests` DISABLE KEYS */;
INSERT INTO `interests` VALUES (2,'현대차','92,400  ','19조 2,515억  ','1,850,954  ','2020-04-24 16:11:40',5),(3,'케이티','23,150  ','6조 1,622억  ','264,669  ','2020-04-27 10:32:41',5),(5,'삼성전자','49,350  ','295조 8,027억  ','4,410,933  ','2020-04-27 10:34:02',5),(6,'LG전자','52,600  ','8조 7,552억  ','319,624  ','2020-04-27 13:18:40',5),(7,'현대차','90,100  ','19조 7,002억  ','1,022,156  ','2020-04-27 14:36:27',8),(8,'현대차','90,100  ','19조 6,788억  ','1,026,474  ','2020-04-27 14:39:56',8),(9,'현대차','90,100  ','19조 6,788억  ','1,028,859  ','2020-04-27 14:40:18',8),(10,'현대차','90,100  ','19조 6,788억  ','1,028,859  ','2020-04-27 14:40:45',8),(11,'삼성전자','49,350  ','298조 1,906억  ','11,505,331  ','2020-04-27 14:55:56',6),(12,'삼성전자','49,350  ','297조 5,937억  ','11,759,129  ','2020-04-27 15:01:43',6),(13,'LG유플러스','12,750  ','5조 7,633억  ','1,429,567  ','2020-04-27 15:53:15',5);
/*!40000 ALTER TABLE `interests` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-27 16:04:35

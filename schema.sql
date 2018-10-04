-- MySQL dump 10.13  Distrib 5.5.32, for debian-linux-gnu (x86_64)
--
-- Host: devdb.sendwell.com    Database: dns4new
-- ------------------------------------------------------
-- Server version	5.5.32-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `geo_city`
--

DROP TABLE IF EXISTS `geo_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `geo_city` (
  `geo_city_id` int(11) NOT NULL AUTO_INCREMENT,
  `city` varchar(256) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `zip` varchar(5) DEFAULT NULL,
  `area_code` varchar(3) DEFAULT NULL,
  `geo_country_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`geo_city_id`),
  KEY `geo_country_id` (`geo_country_id`),
  CONSTRAINT `geo_city_ibfk_1` FOREIGN KEY (`geo_country_id`) REFERENCES `geo_country` (`geo_country_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `geo_coordinates`
--

DROP TABLE IF EXISTS `geo_coordinates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `geo_coordinates` (
  `geo_coordinate_id` int(11) NOT NULL AUTO_INCREMENT,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `geo_city_id` int(11) DEFAULT '0',
  `geo_country_id` int(11) DEFAULT '0',
  PRIMARY KEY (`geo_coordinate_id`),
  KEY `geo_city_id` (`geo_city_id`),
  KEY `geo_country_id` (`geo_country_id`),
  CONSTRAINT `geo_coordinates_ibfk_2` FOREIGN KEY (`geo_country_id`) REFERENCES `geo_country` (`geo_country_id`),
  CONSTRAINT `geo_coordinates_ibfk_1` FOREIGN KEY (`geo_city_id`) REFERENCES `geo_city` (`geo_city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `geo_country`
--

DROP TABLE IF EXISTS `geo_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `geo_country` (
  `geo_country_id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(256) DEFAULT NULL,
  `code` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`geo_country_id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rr`
--

DROP TABLE IF EXISTS `rr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rr` (
  `soa_id` int(11) NOT NULL,
  `serial` int(11) NOT NULL,
  `name` varchar(256) DEFAULT NULL,
  `priority` tinyint(4) DEFAULT '0',
  `type_id` int(11) DEFAULT '0',
  `rr_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`rr_id`),
  KEY `type_id` (`type_id`),
  KEY `soa_id` (`soa_id`),
  CONSTRAINT `rr_ibfk_3` FOREIGN KEY (`type_id`) REFERENCES `rtype` (`type_id`),
  CONSTRAINT `rr_ibfk_4` FOREIGN KEY (`soa_id`) REFERENCES `soa` (`soa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rr_address`
--

DROP TABLE IF EXISTS `rr_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rr_address` (
  `rr_address_id` int(11) NOT NULL AUTO_INCREMENT,
  `rr_address` varchar(256) DEFAULT NULL,
  `geo_coordinate_id` int(11) NOT NULL,
  PRIMARY KEY (`rr_address_id`),
  KEY `geo_coordinate_id` (`geo_coordinate_id`),
  CONSTRAINT `rr_address_ibfk_1` FOREIGN KEY (`geo_coordinate_id`) REFERENCES `geo_coordinates` (`geo_coordinate_id`)
) ENGINE=InnoDB AUTO_INCREMENT=146 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rr_history`
--

DROP TABLE IF EXISTS `rr_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rr_history` (
  `rr_id` int(11) NOT NULL,
  `rr_address_id` int(11) NOT NULL,
  `timestamp` int(11) NOT NULL,
  KEY `rr_id` (`rr_id`),
  KEY `rr_address_id` (`rr_address_id`),
  CONSTRAINT `rr_history_ibfk_1` FOREIGN KEY (`rr_id`) REFERENCES `rr` (`rr_id`),
  CONSTRAINT `rr_history_ibfk_2` FOREIGN KEY (`rr_address_id`) REFERENCES `rr_address` (`rr_address_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rtype`
--

DROP TABLE IF EXISTS `rtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rtype` (
  `type_id` int(11) NOT NULL AUTO_INCREMENT,
  `data` varchar(5) NOT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `soa`
--

DROP TABLE IF EXISTS `soa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `soa` (
  `soa_id` int(11) NOT NULL AUTO_INCREMENT,
  `origin` varchar(256) NOT NULL,
  `refresh` int(11) NOT NULL DEFAULT '28800',
  `retry` int(11) NOT NULL DEFAULT '7200',
  `expire` int(11) NOT NULL DEFAULT '604800',
  `minimum` int(11) NOT NULL DEFAULT '86400',
  `ttl` int(11) NOT NULL DEFAULT '86400',
  `last_check` int(11) DEFAULT '0',
  `locked` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`soa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `whois`
--

DROP TABLE IF EXISTS `whois`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `whois` (
  `soa_id` int(11) NOT NULL,
  `whois_company_id` int(11) NOT NULL,
  `contact` varchar(256) DEFAULT NULL,
  KEY `soa_id` (`soa_id`),
  KEY `whois_company_id` (`whois_company_id`),
  CONSTRAINT `whois_ibfk_1` FOREIGN KEY (`soa_id`) REFERENCES `soa` (`soa_id`),
  CONSTRAINT `whois_ibfk_2` FOREIGN KEY (`whois_company_id`) REFERENCES `whois_company` (`whois_company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `whois_company`
--

DROP TABLE IF EXISTS `whois_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `whois_company` (
  `whois_company_id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`whois_company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-08-29 11:39:54

-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               10.11.6-MariaDB-0+deb12u1 - Debian 12
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

CREATE DATABASE IF NOT EXISTS `power` /*!40100 DEFAULT CHARACTER SET armscii8 COLLATE armscii8_bin */;
USE `power`;

-- Dumping structure for table power.ups
CREATE TABLE IF NOT EXISTS `ups` (
  `date` datetime DEFAULT NULL,
  `type` varchar(26) DEFAULT NULL,
  `value` decimal(20,2) DEFAULT NULL,
  KEY `type` (`type`),
  KEY `date` (`date`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci ROW_FORMAT=COMPRESSED;

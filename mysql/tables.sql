CREATE DATABASE `metalsdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `metals_codes` (
  `code` smallint NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- metalsdb.metals_data definition

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

-- metalsdb.metalls_v source

CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `metalls_v` AS
select
    `md`.`dt` AS `dt`,
    `md`.`buy` AS `buy`,
    `md`.`sell` AS `sell`,
    `mc`.`name` AS `name`
from
    (`metals_codes` `mc`
join `metals_data` `md`)
where
    (`mc`.`code` = `md`.`code`);

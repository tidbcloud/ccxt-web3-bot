
CREATE DATABASE IF NOT EXISTS crypto_demo;

CREATE TABLE IF NOT EXISTS `crypto_demo`.`crypto_trends` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each record',
  `crypto` varchar(100) NOT NULL COMMENT 'Unique identifier for the cryptocurrency',
  `time` timestamp NULL DEFAULT NULL COMMENT 'Timestamp of the recorded data',
  `open_price` float DEFAULT NULL COMMENT 'Opening price of the cryptocurrency during the specified time interval',
  `high_price` float DEFAULT NULL COMMENT 'Highest price of the cryptocurrency during the specified time interval',
  `low_price` float DEFAULT NULL COMMENT 'Lowest price of the cryptocurrency during the specified time interval',
  `close_price` float DEFAULT NULL COMMENT 'Closing price of the cryptocurrency during the specified time interval',
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  UNIQUE KEY `exchange_crypto_id_time` (`crypto`,`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;

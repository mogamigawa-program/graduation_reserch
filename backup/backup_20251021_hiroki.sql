/*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: user_info
-- ------------------------------------------------------
-- Server version	11.4.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Current Database: `user_info`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `user_info` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `user_info`;

--
-- Table structure for table `user_databases`
--

DROP TABLE IF EXISTS `user_databases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_databases` (
  `user_id` int(11) NOT NULL,
  `database_name` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`,`database_name`),
  CONSTRAINT `user_databases_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_databases`
--

LOCK TABLES `user_databases` WRITE;
/*!40000 ALTER TABLE `user_databases` DISABLE KEYS */;
INSERT INTO `user_databases` VALUES
(27,'admin_db'),
(36,'aaa_db'),
(37,'guest_db'),
(38,'2_db'),
(39,'3_db'),
(40,'4_db'),
(41,'5_db'),
(42,'6_db'),
(43,'7_db'),
(44,'a_db'),
(45,'aa_db'),
(46,'test_db');
/*!40000 ALTER TABLE `user_databases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(27,'admin','$2b$12$z73TVOGJU6rVHWQ77kDpPOVyWm0DVJZwKGTjgaVr20L8/rgHgWk6q',1),
(36,'aaa','$2b$12$syUtEGEcO/6x6amvkI/lkeqYZYvRZxVD5ILMw5UGKDcUqEWzX2pSa',0),
(37,'guest','$2b$12$f1BTuexSNaSSPNH/iAmoL.NrBY5HB6pGApFhfllvzZxSUrCdljEiW',0),
(38,'2','$2b$12$2eKW3eYeWLwKos83oe19QuNd/V1.tIQLArr87QmCBGeos14HZALDa',0),
(39,'3','$2b$12$Nby0Bb/xbgEZBWtY.g0PU.ia.KEuZUk4x.LXwy3oxp/FivHTyGdvi',0),
(40,'4','$2b$12$qw9CZ7zgg/UuxQQszL.uc.8lIYjc2oKiDzuPpIXL5TvSQc1LnFa3e',0),
(41,'5','$2b$12$jyp.ReVn6W3xmJuH9UBZqurSOCQTt5qS4B.DduMc4H2WwRJDR06vK',0),
(42,'6','$2b$12$ptJZd7rb.LbxKMNbHaEmzuk0ote.6EicN.eo2D.AmPkroiPa4E3F2',0),
(43,'7','$2b$12$2n3a1/e16kDP86WjK5HrruzI5u.rKlCoRAL.hI/MVRq/d59neThEm',0),
(44,'a','$2b$12$5d7tr8D9udQTAMwn71KVJelbD6YF30ZpvQLx.4YII.HLeJE4lff5K',0),
(45,'aa','$2b$12$.cdH4zIH04QXdcRM8oO97ugIcEsDWi.fXw57jzHMBQCwdkAPKdRD6',0),
(46,'test','$2b$12$91M5rM0hDRs7gf0T7sJluOJfMNNnOZlpvLu7cQ1.NwietVga5de7O',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Current Database: `dataset`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dataset` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `dataset`;

--
-- Table structure for table `all_users`
--

DROP TABLE IF EXISTS `all_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `all_users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `all_users`
--

LOCK TABLES `all_users` WRITE;
/*!40000 ALTER TABLE `all_users` DISABLE KEYS */;
INSERT INTO `all_users` VALUES
(1,'田中太郎',17),
(2,'鈴木花子',20),
(3,'佐藤一郎',18),
(4,'山田次郎',22),
(5,'高橋三郎',15),
(6,'伊藤美咲',30),
(7,'中村健太',16),
(8,'小林直子',25),
(9,'加藤悠真',19),
(10,'松本由紀',13);
/*!40000 ALTER TABLE `all_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `choices`
--

DROP TABLE IF EXISTS `choices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `choices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `choice_text` text NOT NULL,
  `is_correct` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_question_id` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=256 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choices`
--

LOCK TABLES `choices` WRITE;
/*!40000 ALTER TABLE `choices` DISABLE KEYS */;
INSERT INTO `choices` VALUES
(1,1,'SELECT * FROM users',0),
(2,1,'DELETE FROM users WHERE id = 1',0),
(3,1,'INSERT INTO users (name) VALUES (\"Alice\")',1),
(4,1,'UPDATE users SET name = \"Bob\" WHERE id = 1',0),
(5,2,'SELECT name FROM users',0),
(6,2,'UPDATE users SET name = \"Charlie\" WHERE id = 1',1),
(7,2,'INSERT INTO users (name) VALUES (\"Charlie\")',0),
(8,2,'DELETE FROM users WHERE id = 1',0),
(9,3,'INSERT INTO users (name) VALUES (\"Alice\");',1),
(10,3,'SELECT * FROM users;',0),
(11,3,'UPDATE users SET name = \"Alice\";',0),
(12,3,'DELETE FROM users WHERE name = \"Alice\";',0),
(13,4,'INSERT INTO users (name, age) VALUES (\"Tom\", 30);',1),
(14,4,'INSERT INTO users name, age VALUES (\"Tom\", 30);',0),
(15,4,'INSERT users (name, age) VALUES (\"Tom\", 30);',0),
(16,4,'INSERT INTO users VALUES name, age (\"Tom\", 30);',0),
(17,5,'はい、省略可能です。',1),
(18,5,'いいえ、必ず列名が必要です。',0),
(19,5,'WHERE句を使えば省略できます。',0),
(20,5,'テーブルの構造に関係なく常に列名は必要です。',0),
(21,6,'INSERT INTO users (name) VALUES (\"Tom\"), (\"Jerry\");',1),
(22,6,'INSERT INTO users (name) VALUE (\"Tom\"); (\"Jerry\");',0),
(23,6,'INSERT ALL INTO users VALUES (\"Tom\"), (\"Jerry\");',0),
(24,6,'INSERT INTO users (name) ADD (\"Tom\"), (\"Jerry\");',0),
(25,7,'テーブルの列数とVALUESの数が合っていない可能性があるから',1),
(26,7,'文字列をダブルクォーテーションで囲んでいるから',0),
(27,7,'usersテーブルにデータを削除していないから',0),
(28,7,'VALUESではなくVALUEを使っているから',0),
(29,8,'REMOVE FROM users WHERE id = 3;',0),
(30,8,'DELETE users WHERE id = 3;',0),
(31,8,'DELETE FROM users WHERE id = 3;',1),
(32,8,'DELETE WHERE id = 3 FROM users;',0),
(33,9,'DELETE FROM users WHERE name = Taro;',0),
(34,9,'DELETE FROM users WHERE name = \"Taro\";',1),
(35,9,'DELETE users WHERE name = \'Taro\';',0),
(36,9,'DELETE FROM users name = \'Taro\';',0),
(37,10,'priceが0の商品のみを削除する',1),
(38,10,'productsテーブルを削除する',0),
(39,10,'priceがNULLのデータを削除する',0),
(40,10,'全てのデータを削除する',0),
(41,11,'全てのデータが削除される',1),
(42,11,'何も削除されない',0),
(43,11,'構文エラーになる',0),
(44,11,'1行だけ削除される',0),
(45,12,'WHERE句を忘れないようにする',1),
(46,12,'UPDATE文を使う',0),
(47,12,'SELECTで先に確認する',0),
(48,12,'DELETEを2回実行する',0),
(49,13,'DELETE users WHERE age >= 30 AND status = \"active\";',0),
(50,13,'DELETE FROM users WHERE age = 30 status = \"active\";',0),
(51,13,'DELETE FROM users WHERE age >= 30 OR status = \"active\";',0),
(52,13,'DELETE FROM users WHERE age >= 30 AND status = \"active\";',1),
(53,14,'DELETE FROM users WHERE age < 20 AND address IS NULL;',0),
(54,14,'DELETE FROM users WHERE age < 20 OR address = \"NULL\";',0),
(55,14,'DELETE FROM users WHERE age < 20 OR address IS NULL;',1),
(56,14,'DELETE FROM users WHERE age < 20 AND address = NULL;',0),
(57,15,'年齢に関係なく全てのユーザーを削除する',0),
(58,15,'ageが18以上のKenという名前のユーザーを削除する',0),
(59,15,'nameが\"Ken\"またはageが18未満のユーザーを削除する',1),
(60,15,'nameが\"Ken\"かつageが18未満のユーザーを削除する',0),
(61,16,'statusが\"inactive\"のユーザーをすべて削除',0),
(62,16,'年齢が60未満でstatusが\"active\"のユーザーを削除',0),
(63,16,'年齢が20未満またはstatusが\"inactive\"のユーザーを削除',0),
(64,16,'年齢が20未満または60より大きく、かつstatusが\"inactive\"のユーザーを削除',1),
(65,17,'DELETE文では複数条件を使えない',0),
(66,17,'WHEREを省略しても一部のデータだけ削除できる',0),
(67,17,'ORは必ずANDより先に評価されるので()は不要',0),
(68,17,'複雑な条件では()を使って優先順位を明確にする',1),
(69,18,'INSERT + SELECT は列を追加する',0),
(70,18,'INSERT はテーブルを削除する',0),
(71,18,'SELECT は新しいテーブルを作成する',0),
(72,18,'INSERT + SELECT はデータをコピーする',1),
(73,19,'INSERT x SELECT FROM y;',0),
(74,19,'INSERT INTO x VALUES (SELECT id FROM y);',0),
(75,19,'SELECT INTO x FROM y;',0),
(76,19,'INSERT INTO x (id) SELECT id FROM y;',1),
(77,20,'old_table を削除する',0),
(78,20,'old_table の name列を new_table にコピーする',1),
(79,20,'new_table を作成する',0),
(80,20,'name列を削除して挿入する',0),
(81,21,'WHERE 句が必要',0),
(82,21,'SELECT 文が間違っている',0),
(83,21,'テーブルが存在しない',0),
(84,21,'コピー先に列が足りない',1),
(85,22,'18歳未満のユーザーのみ logs に入る',1),
(86,22,'全ユーザーが logs に入る',0),
(87,22,'members テーブルが変更される',0),
(88,22,'実行エラーが発生する',0),
(89,23,'完了した注文を archive にコピーする',1),
(90,23,'新しい注文を作成する',0),
(91,23,'archive を削除する',0),
(92,23,'orders テーブルを削除する',0),
(93,24,'UPDATE products WHERE product_id = 1 SET price = 1000;',0),
(94,24,'UPDATE products SET price = 1000 WHERE product_id = 1;',1),
(95,24,'UPDATE SET products.price = 1000 WHERE product_id = 1;',0),
(96,24,'MODIFY products SET price = 1000 WHERE product_id = 1;',0),
(97,25,'UPDATE products SET \'status\' = \'active\' WHERE \'status\' = \'inactive\';',0),
(98,25,'UPDATE products SET status = active WHERE status = inactive;',0),
(99,25,'UPDATE products SET status = \'active\' WHERE status = \'inactive\';',1),
(100,25,'UPDATE status FROM products TO \'active\' IF status = \'inactive\';',0),
(101,26,'UPDATE products SET price = 50000 WHERE product_name = \'パソコン\';',1),
(102,26,'UPDATE products SET price = 50000 IF product_name = \'パソコン\';',0),
(103,26,'UPDATE products SET price = \'50000\' WHERE product_name = パソコン;',0),
(104,26,'MODIFY products SET price TO 50000 WHERE product_name = \'パソコン\';',0),
(105,27,'UPDATE products SET stock TO 10 WHERE price == 5000;',0),
(106,27,'UPDATE products WHERE price = 5000 SET stock = 10;',0),
(107,27,'UPDATE stock = 10 FROM products WHERE price = 5000;',0),
(108,27,'UPDATE products SET stock = 10 WHERE price = 5000;',1),
(109,28,'UPDATE products SET status = \'inactive\' WHERE stock = 50;',1),
(110,28,'UPDATE products SET status TO inactive IF stock IS 50;',0),
(111,28,'UPDATE products WHERE stock = 50 SET status = \'inactive\';',0),
(112,28,'UPDATE SET status = \'inactive\' WHERE stock = 50 FROM products;',0),
(113,29,'UPDATE products SET product_name = \"New Name\" AND price = 2000 WHERE product_id = 1;',0),
(114,29,'UPDATE products SET product_name = \"New Name\", price = 2000 WHERE product_id = 1;',1),
(115,29,'UPDATE products (product_name, price) VALUES (\"New Name\", 2000) WHERE product_id = 1;',0),
(116,29,'UPDATE products SET (product_name = \"New Name\", price = 2000) WHERE product_id = 1;',0),
(117,30,'UPDATE products SET stock = 80, price = 190000 WHERE product_id = 2;',0),
(118,30,'UPDATE products SET stock = 80 AND price = 190000 WHERE product_id = 2 AND status = \"active\";',0),
(119,30,'UPDATE products SET (stock = 80, price = 190000) WHERE product_id = 2 AND status = \"active\";',0),
(120,30,'UPDATE products SET stock = 80, price = 190000 WHERE product_id = 2 AND status = \"active\";',1),
(121,31,'UPDATE products SET status = \"active\", price = 4000 WHERE price >= 5000 AND status = \"inactive\";',1),
(122,31,'UPDATE products SET (status = \"active\", price = 4000) WHERE price >= 5000 AND status = \"inactive\";',0),
(123,31,'UPDATE products SET status = \"active\" AND price = 4000 WHERE price >= 5000 AND status = \"inactive\";',0),
(124,31,'UPDATE products SET status = \"active\", price = 4000 WHERE (price >= 5000, status = \"inactive\");',0),
(125,32,'UPDATE products SET stock = 20, status = \"out\" WHERE product_id = 3;',0),
(126,32,'UPDATE products SET stock = 20 AND status = \"out\" WHERE product_id = 3 AND stock = 10;',0),
(127,32,'UPDATE products SET stock = 20, status = \"out\" WHERE product_id = 3 AND stock = 10;',1),
(128,32,'UPDATE products (stock, status) VALUES (20, \"out\") WHERE product_id = 3 AND stock = 10;',0),
(129,33,'UPDATE products SET status = \"sold out\", stock = 5 WHERE stock = 0;',0),
(130,33,'UPDATE products SET status = \"sold out\", stock = 5 WHERE stock = 0 AND status = \"inactive\";',1),
(131,33,'UPDATE products SET status = \"sold out\" AND stock = 5 WHERE stock = 0 AND status = \"inactive\";',0),
(132,33,'UPDATE products SET (status = \"sold out\", stock = 5) WHERE stock = 0 AND status = \"inactive\";',0);
/*!40000 ALTER TABLE `choices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `choices_backup`
--

DROP TABLE IF EXISTS `choices_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `choices_backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `choice_text` text NOT NULL,
  `is_correct` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10020 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choices_backup`
--

LOCK TABLES `choices_backup` WRITE;
/*!40000 ALTER TABLE `choices_backup` DISABLE KEYS */;
INSERT INTO `choices_backup` VALUES
(1,1,'SELECT * FROM users',0),
(2,1,'DELETE FROM users WHERE id = 1',0),
(3,1,'INSERT INTO users (name) VALUES (\"Alice\")',1),
(4,1,'UPDATE users SET name = \"Bob\" WHERE id = 1',0),
(5,2,'SELECT name FROM users',0),
(6,2,'UPDATE users SET name = \"Charlie\" WHERE id = 1',1),
(7,2,'INSERT INTO users (name) VALUES (\"Charlie\")',0),
(8,2,'DELETE FROM users WHERE id = 1',0),
(9,3,'INSERT INTO users (name) VALUES (\"Alice\");',1),
(10,3,'SELECT * FROM users;',0),
(11,3,'UPDATE users SET name = \"Alice\";',0),
(12,3,'DELETE FROM users WHERE name = \"Alice\";',0),
(13,4,'INSERT INTO users (name, age) VALUES (\"Tom\", 30);',1),
(14,4,'INSERT INTO users name, age VALUES (\"Tom\", 30);',0),
(15,4,'INSERT users (name, age) VALUES (\"Tom\", 30);',0),
(16,4,'INSERT INTO users VALUES name, age (\"Tom\", 30);',0),
(17,5,'はい、省略可能です。',1),
(18,5,'いいえ、必ず列名が必要です。',0),
(19,5,'WHERE句を使えば省略できます。',0),
(20,5,'テーブルの構造に関係なく常に列名は必要です。',0),
(21,6,'INSERT INTO users (name) VALUES (\"Tom\"), (\"Jerry\");',1),
(22,6,'INSERT INTO users (name) VALUE (\"Tom\"); (\"Jerry\");',0),
(23,6,'INSERT ALL INTO users VALUES (\"Tom\"), (\"Jerry\");',0),
(24,6,'INSERT INTO users (name) ADD (\"Tom\"), (\"Jerry\");',0),
(25,7,'テーブルの列数とVALUESの数が合っていない可能性があるから',1),
(26,7,'文字列をダブルクォーテーションで囲んでいるから',0),
(27,7,'usersテーブルにデータを削除していないから',0),
(28,7,'VALUESではなくVALUEを使っているから',0),
(29,8,'REMOVE FROM users WHERE id = 3;',0),
(30,8,'DELETE users WHERE id = 3;',0),
(31,8,'DELETE FROM users WHERE id = 3;',1),
(32,8,'DELETE WHERE id = 3 FROM users;',0),
(33,9,'DELETE FROM users WHERE name = Taro;',0),
(34,9,'DELETE FROM users WHERE name = \"Taro\";',1),
(35,9,'DELETE users WHERE name = \'Taro\';',0),
(36,9,'DELETE FROM users name = \'Taro\';',0),
(37,10,'priceが0の商品のみを削除する',1),
(38,10,'productsテーブルを削除する',0),
(39,10,'priceがNULLのデータを削除する',0),
(40,10,'全てのデータを削除する',0),
(41,11,'全てのデータが削除される',1),
(42,11,'何も削除されない',0),
(43,11,'構文エラーになる',0),
(44,11,'1行だけ削除される',0),
(45,12,'WHERE句を忘れないようにする',1),
(46,12,'UPDATE文を使う',0),
(47,12,'SELECTで先に確認する',0),
(48,12,'DELETEを2回実行する',0),
(1001,13,'DELETE users WHERE age >= 30 AND status = \"active\";',0),
(1002,13,'DELETE FROM users WHERE age = 30 status = \"active\";',0),
(1003,13,'DELETE FROM users WHERE age >= 30 OR status = \"active\";',0),
(1004,13,'DELETE FROM users WHERE age >= 30 AND status = \"active\";',1),
(1005,14,'DELETE FROM users WHERE age < 20 AND address IS NULL;',0),
(1006,14,'DELETE FROM users WHERE age < 20 OR address = \"NULL\";',0),
(1007,14,'DELETE FROM users WHERE age < 20 OR address IS NULL;',1),
(1008,14,'DELETE FROM users WHERE age < 20 AND address = NULL;',0),
(1009,15,'年齢に関係なく全てのユーザーを削除する',0),
(1010,15,'ageが18以上のKenという名前のユーザーを削除する',0),
(1011,15,'nameが\"Ken\"またはageが18未満のユーザーを削除する',1),
(1012,15,'nameが\"Ken\"かつageが18未満のユーザーを削除する',0),
(1013,16,'statusが\"inactive\"のユーザーをすべて削除',0),
(1014,16,'年齢が60未満でstatusが\"active\"のユーザーを削除',0),
(1015,16,'年齢が20未満またはstatusが\"inactive\"のユーザーを削除',0),
(1016,16,'年齢が20未満または60より大きく、かつstatusが\"inactive\"のユーザーを削除',1),
(1017,17,'DELETE文では複数条件を使えない',0),
(1018,17,'WHEREを省略しても一部のデータだけ削除できる',0),
(1019,17,'ORは必ずANDより先に評価されるので()は不要',0),
(1020,17,'複雑な条件では()を使って優先順位を明確にする',1),
(1021,18,'INSERT + SELECT は列を追加する',0),
(1022,18,'INSERT はテーブルを削除する',0),
(1023,18,'SELECT は新しいテーブルを作成する',0),
(1024,18,'INSERT + SELECT はデータをコピーする',1),
(1025,19,'INSERT x SELECT FROM y;',0),
(1026,19,'INSERT INTO x VALUES (SELECT id FROM y);',0),
(1027,19,'SELECT INTO x FROM y;',0),
(1028,19,'INSERT INTO x (id) SELECT id FROM y;',1),
(1029,20,'old_table を削除する',0),
(1030,20,'old_table の name列を new_table にコピーする',1),
(1031,20,'new_table を作成する',0),
(1032,20,'name列を削除して挿入する',0),
(1033,21,'WHERE 句が必要',0),
(1034,21,'SELECT 文が間違っている',0),
(1035,21,'テーブルが存在しない',0),
(1036,21,'コピー先に列が足りない',1),
(1037,22,'18歳未満のユーザーのみ logs に入る',1),
(1038,22,'全ユーザーが logs に入る',0),
(1039,22,'members テーブルが変更される',0),
(1040,22,'実行エラーが発生する',0),
(1041,23,'完了した注文を archive にコピーする',1),
(1042,23,'新しい注文を作成する',0),
(1043,23,'archive を削除する',0),
(1044,23,'orders テーブルを削除する',0),
(1045,24,'UPDATE products WHERE product_id = 1 SET price = 1000;',0),
(1046,24,'UPDATE products SET price = 1000 WHERE product_id = 1;',1),
(1047,24,'UPDATE SET products.price = 1000 WHERE product_id = 1;',0),
(1048,24,'MODIFY products SET price = 1000 WHERE product_id = 1;',0),
(1049,25,'UPDATE products SET \'status\' = \'active\' WHERE \'status\' = \'inactive\';',0),
(1050,25,'UPDATE products SET status = active WHERE status = inactive;',0),
(1051,25,'UPDATE products SET status = \'active\' WHERE status = \'inactive\';',1),
(1052,25,'UPDATE status FROM products TO \'active\' IF status = \'inactive\';',0),
(1053,26,'UPDATE products SET price = 50000 WHERE product_name = \'パソコン\';',1),
(1054,26,'UPDATE products SET price = 50000 IF product_name = \'パソコン\';',0),
(1055,26,'UPDATE products SET price = \'50000\' WHERE product_name = パソコン;',0),
(1056,26,'MODIFY products SET price TO 50000 WHERE product_name = \'パソコン\';',0),
(1057,27,'UPDATE products SET stock TO 10 WHERE price == 5000;',0),
(1058,27,'UPDATE products WHERE price = 5000 SET stock = 10;',0),
(1059,27,'UPDATE stock = 10 FROM products WHERE price = 5000;',0),
(1060,27,'UPDATE products SET stock = 10 WHERE price = 5000;',1),
(1061,28,'UPDATE products SET status = \'inactive\' WHERE stock = 50;',1),
(1062,28,'UPDATE products SET status TO inactive IF stock IS 50;',0),
(1063,28,'UPDATE products WHERE stock = 50 SET status = \'inactive\';',0),
(1064,28,'UPDATE SET status = \'inactive\' WHERE stock = 50 FROM products;',0),
(10000,29,'UPDATE products SET product_name = \"New Name\" AND price = 2000 WHERE product_id = 1;',0),
(10001,29,'UPDATE products SET product_name = \"New Name\", price = 2000 WHERE product_id = 1;',1),
(10002,29,'UPDATE products (product_name, price) VALUES (\"New Name\", 2000) WHERE product_id = 1;',0),
(10003,29,'UPDATE products SET (product_name = \"New Name\", price = 2000) WHERE product_id = 1;',0),
(10004,30,'UPDATE products SET stock = 80, price = 190000 WHERE product_id = 2;',0),
(10005,30,'UPDATE products SET stock = 80 AND price = 190000 WHERE product_id = 2 AND status = \"active\";',0),
(10006,30,'UPDATE products SET (stock = 80, price = 190000) WHERE product_id = 2 AND status = \"active\";',0),
(10007,30,'UPDATE products SET stock = 80, price = 190000 WHERE product_id = 2 AND status = \"active\";',1),
(10008,31,'UPDATE products SET status = \"active\", price = 4000 WHERE price >= 5000 AND status = \"inactive\";',1),
(10009,31,'UPDATE products SET (status = \"active\", price = 4000) WHERE price >= 5000 AND status = \"inactive\";',0),
(10010,31,'UPDATE products SET status = \"active\" AND price = 4000 WHERE price >= 5000 AND status = \"inactive\";',0),
(10011,31,'UPDATE products SET status = \"active\", price = 4000 WHERE (price >= 5000, status = \"inactive\");',0),
(10012,32,'UPDATE products SET stock = 20, status = \"out\" WHERE product_id = 3;',0),
(10013,32,'UPDATE products SET stock = 20 AND status = \"out\" WHERE product_id = 3 AND stock = 10;',0),
(10014,32,'UPDATE products SET stock = 20, status = \"out\" WHERE product_id = 3 AND stock = 10;',1),
(10015,32,'UPDATE products (stock, status) VALUES (20, \"out\") WHERE product_id = 3 AND stock = 10;',0),
(10016,33,'UPDATE products SET status = \"sold out\", stock = 5 WHERE stock = 0;',0),
(10017,33,'UPDATE products SET status = \"sold out\", stock = 5 WHERE stock = 0 AND status = \"inactive\";',1),
(10018,33,'UPDATE products SET status = \"sold out\" AND stock = 5 WHERE stock = 0 AND status = \"inactive\";',0),
(10019,33,'UPDATE products SET (status = \"sold out\", stock = 5) WHERE stock = 0 AND status = \"inactive\";',0);
/*!40000 ALTER TABLE `choices_backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `choices_old`
--

DROP TABLE IF EXISTS `choices_old`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `choices_old` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `choice_text` text NOT NULL,
  `is_correct` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `choices_old_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10020 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choices_old`
--

LOCK TABLES `choices_old` WRITE;
/*!40000 ALTER TABLE `choices_old` DISABLE KEYS */;
INSERT INTO `choices_old` VALUES
(1,1,'SELECT * FROM users',0),
(2,1,'DELETE FROM users WHERE id = 1',0),
(3,1,'INSERT INTO users (name) VALUES (\"Alice\")',1),
(4,1,'UPDATE users SET name = \"Bob\" WHERE id = 1',0),
(5,2,'SELECT name FROM users',0),
(6,2,'UPDATE users SET name = \"Charlie\" WHERE id = 1',1),
(7,2,'INSERT INTO users (name) VALUES (\"Charlie\")',0),
(8,2,'DELETE FROM users WHERE id = 1',0),
(9,3,'INSERT INTO users (name) VALUES (\"Alice\");',1),
(10,3,'SELECT * FROM users;',0),
(11,3,'UPDATE users SET name = \"Alice\";',0),
(12,3,'DELETE FROM users WHERE name = \"Alice\";',0),
(13,4,'INSERT INTO users (name, age) VALUES (\"Tom\", 30);',1),
(14,4,'INSERT INTO users name, age VALUES (\"Tom\", 30);',0),
(15,4,'INSERT users (name, age) VALUES (\"Tom\", 30);',0),
(16,4,'INSERT INTO users VALUES name, age (\"Tom\", 30);',0),
(17,5,'はい、省略可能です。',1),
(18,5,'いいえ、必ず列名が必要です。',0),
(19,5,'WHERE句を使えば省略できます。',0),
(20,5,'テーブルの構造に関係なく常に列名は必要です。',0),
(21,6,'INSERT INTO users (name) VALUES (\"Tom\"), (\"Jerry\");',1),
(22,6,'INSERT INTO users (name) VALUE (\"Tom\"); (\"Jerry\");',0),
(23,6,'INSERT ALL INTO users VALUES (\"Tom\"), (\"Jerry\");',0),
(24,6,'INSERT INTO users (name) ADD (\"Tom\"), (\"Jerry\");',0),
(25,7,'テーブルの列数とVALUESの数が合っていない可能性があるから',1),
(26,7,'文字列をダブルクォーテーションで囲んでいるから',0),
(27,7,'usersテーブルにデータを削除していないから',0),
(28,7,'VALUESではなくVALUEを使っているから',0),
(29,8,'REMOVE FROM users WHERE id = 3;',0),
(30,8,'DELETE users WHERE id = 3;',0),
(31,8,'DELETE FROM users WHERE id = 3;',1),
(32,8,'DELETE WHERE id = 3 FROM users;',0),
(33,9,'DELETE FROM users WHERE name = Taro;',0),
(34,9,'DELETE FROM users WHERE name = \"Taro\";',1),
(35,9,'DELETE users WHERE name = \'Taro\';',0),
(36,9,'DELETE FROM users name = \'Taro\';',0),
(37,10,'priceが0の商品のみを削除する',1),
(38,10,'productsテーブルを削除する',0),
(39,10,'priceがNULLのデータを削除する',0),
(40,10,'全てのデータを削除する',0),
(41,11,'全てのデータが削除される',1),
(42,11,'何も削除されない',0),
(43,11,'構文エラーになる',0),
(44,11,'1行だけ削除される',0),
(45,12,'WHERE句を忘れないようにする',1),
(46,12,'UPDATE文を使う',0),
(47,12,'SELECTで先に確認する',0),
(48,12,'DELETEを2回実行する',0),
(1001,13,'DELETE users WHERE age >= 30 AND status = \"active\";',0),
(1002,13,'DELETE FROM users WHERE age = 30 status = \"active\";',0),
(1003,13,'DELETE FROM users WHERE age >= 30 OR status = \"active\";',0),
(1004,13,'DELETE FROM users WHERE age >= 30 AND status = \"active\";',1),
(1005,14,'DELETE FROM users WHERE age < 20 AND address IS NULL;',0),
(1006,14,'DELETE FROM users WHERE age < 20 OR address = \"NULL\";',0),
(1007,14,'DELETE FROM users WHERE age < 20 OR address IS NULL;',1),
(1008,14,'DELETE FROM users WHERE age < 20 AND address = NULL;',0),
(1009,15,'年齢に関係なく全てのユーザーを削除する',0),
(1010,15,'ageが18以上のKenという名前のユーザーを削除する',0),
(1011,15,'nameが\"Ken\"またはageが18未満のユーザーを削除する',1),
(1012,15,'nameが\"Ken\"かつageが18未満のユーザーを削除する',0),
(1013,16,'statusが\"inactive\"のユーザーをすべて削除',0),
(1014,16,'年齢が60未満でstatusが\"active\"のユーザーを削除',0),
(1015,16,'年齢が20未満またはstatusが\"inactive\"のユーザーを削除',0),
(1016,16,'年齢が20未満または60より大きく、かつstatusが\"inactive\"のユーザーを削除',1),
(1017,17,'DELETE文では複数条件を使えない',0),
(1018,17,'WHEREを省略しても一部のデータだけ削除できる',0),
(1019,17,'ORは必ずANDより先に評価されるので()は不要',0),
(1020,17,'複雑な条件では()を使って優先順位を明確にする',1),
(1021,18,'INSERT + SELECT は列を追加する',0),
(1022,18,'INSERT はテーブルを削除する',0),
(1023,18,'SELECT は新しいテーブルを作成する',0),
(1024,18,'INSERT + SELECT はデータをコピーする',1),
(1025,19,'INSERT x SELECT FROM y;',0),
(1026,19,'INSERT INTO x VALUES (SELECT id FROM y);',0),
(1027,19,'SELECT INTO x FROM y;',0),
(1028,19,'INSERT INTO x (id) SELECT id FROM y;',1),
(1029,20,'old_table を削除する',0),
(1030,20,'old_table の name列を new_table にコピーする',1),
(1031,20,'new_table を作成する',0),
(1032,20,'name列を削除して挿入する',0),
(1033,21,'WHERE 句が必要',0),
(1034,21,'SELECT 文が間違っている',0),
(1035,21,'テーブルが存在しない',0),
(1036,21,'コピー先に列が足りない',1),
(1037,22,'18歳未満のユーザーのみ logs に入る',1),
(1038,22,'全ユーザーが logs に入る',0),
(1039,22,'members テーブルが変更される',0),
(1040,22,'実行エラーが発生する',0),
(1041,23,'完了した注文を archive にコピーする',1),
(1042,23,'新しい注文を作成する',0),
(1043,23,'archive を削除する',0),
(1044,23,'orders テーブルを削除する',0),
(1045,24,'UPDATE products WHERE product_id = 1 SET price = 1000;',0),
(1046,24,'UPDATE products SET price = 1000 WHERE product_id = 1;',1),
(1047,24,'UPDATE SET products.price = 1000 WHERE product_id = 1;',0),
(1048,24,'MODIFY products SET price = 1000 WHERE product_id = 1;',0),
(1049,25,'UPDATE products SET \'status\' = \'active\' WHERE \'status\' = \'inactive\';',0),
(1050,25,'UPDATE products SET status = active WHERE status = inactive;',0),
(1051,25,'UPDATE products SET status = \'active\' WHERE status = \'inactive\';',1),
(1052,25,'UPDATE status FROM products TO \'active\' IF status = \'inactive\';',0),
(1053,26,'UPDATE products SET price = 50000 WHERE product_name = \'パソコン\';',1),
(1054,26,'UPDATE products SET price = 50000 IF product_name = \'パソコン\';',0),
(1055,26,'UPDATE products SET price = \'50000\' WHERE product_name = パソコン;',0),
(1056,26,'MODIFY products SET price TO 50000 WHERE product_name = \'パソコン\';',0),
(1057,27,'UPDATE products SET stock TO 10 WHERE price == 5000;',0),
(1058,27,'UPDATE products WHERE price = 5000 SET stock = 10;',0),
(1059,27,'UPDATE stock = 10 FROM products WHERE price = 5000;',0),
(1060,27,'UPDATE products SET stock = 10 WHERE price = 5000;',1),
(1061,28,'UPDATE products SET status = \'inactive\' WHERE stock = 50;',1),
(1062,28,'UPDATE products SET status TO inactive IF stock IS 50;',0),
(1063,28,'UPDATE products WHERE stock = 50 SET status = \'inactive\';',0),
(1064,28,'UPDATE SET status = \'inactive\' WHERE stock = 50 FROM products;',0),
(10000,29,'UPDATE products SET product_name = \"New Name\" AND price = 2000 WHERE product_id = 1;',0),
(10001,29,'UPDATE products SET product_name = \"New Name\", price = 2000 WHERE product_id = 1;',1),
(10002,29,'UPDATE products (product_name, price) VALUES (\"New Name\", 2000) WHERE product_id = 1;',0),
(10003,29,'UPDATE products SET (product_name = \"New Name\", price = 2000) WHERE product_id = 1;',0),
(10004,30,'UPDATE products SET stock = 80, price = 190000 WHERE product_id = 2;',0),
(10005,30,'UPDATE products SET stock = 80 AND price = 190000 WHERE product_id = 2 AND status = \"active\";',0),
(10006,30,'UPDATE products SET (stock = 80, price = 190000) WHERE product_id = 2 AND status = \"active\";',0),
(10007,30,'UPDATE products SET stock = 80, price = 190000 WHERE product_id = 2 AND status = \"active\";',1),
(10008,31,'UPDATE products SET status = \"active\", price = 4000 WHERE price >= 5000 AND status = \"inactive\";',1),
(10009,31,'UPDATE products SET (status = \"active\", price = 4000) WHERE price >= 5000 AND status = \"inactive\";',0),
(10010,31,'UPDATE products SET status = \"active\" AND price = 4000 WHERE price >= 5000 AND status = \"inactive\";',0),
(10011,31,'UPDATE products SET status = \"active\", price = 4000 WHERE (price >= 5000, status = \"inactive\");',0),
(10012,32,'UPDATE products SET stock = 20, status = \"out\" WHERE product_id = 3;',0),
(10013,32,'UPDATE products SET stock = 20 AND status = \"out\" WHERE product_id = 3 AND stock = 10;',0),
(10014,32,'UPDATE products SET stock = 20, status = \"out\" WHERE product_id = 3 AND stock = 10;',1),
(10015,32,'UPDATE products (stock, status) VALUES (20, \"out\") WHERE product_id = 3 AND stock = 10;',0),
(10016,33,'UPDATE products SET status = \"sold out\", stock = 5 WHERE stock = 0;',0),
(10017,33,'UPDATE products SET status = \"sold out\", stock = 5 WHERE stock = 0 AND status = \"inactive\";',1),
(10018,33,'UPDATE products SET status = \"sold out\" AND stock = 5 WHERE stock = 0 AND status = \"inactive\";',0),
(10019,33,'UPDATE products SET (status = \"sold out\", stock = 5) WHERE stock = 0 AND status = \"inactive\";',0);
/*!40000 ALTER TABLE `choices_old` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cities`
--

DROP TABLE IF EXISTS `cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cities` (
  `id` char(10) DEFAULT NULL,
  `name` char(30) DEFAULT NULL,
  `population` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cities`
--

LOCK TABLES `cities` WRITE;
/*!40000 ALTER TABLE `cities` DISABLE KEYS */;
INSERT INTO `cities` VALUES
('001','Tokyo',13929286),
('002','New York',8419000),
('003','London',8982000),
('004','Paris',2148000),
('005','Berlin',3769000);
/*!40000 ALTER TABLE `cities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `order_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES
(101,1,'2023-08-01'),
(102,2,'2023-08-13'),
(103,3,'2023-08-15');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts`
--

DROP TABLE IF EXISTS `discounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discounts` (
  `discount_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `discount_rate` decimal(3,2) NOT NULL CHECK (`discount_rate` between 0 and 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts`
--

LOCK TABLES `discounts` WRITE;
/*!40000 ALTER TABLE `discounts` DISABLE KEYS */;
INSERT INTO `discounts` VALUES
(201,1,0.10),
(202,2,0.15);
/*!40000 ALTER TABLE `discounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `department` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES
(1,'John Doe',28,'営業'),
(2,'Jane Smith',32,'経理'),
(3,'Michael Johnson',45,'開発'),
(4,'Emily Davis',29,'人事'),
(5,'David Brown',36,'営業'),
(6,'Emma Wilson',25,'経理'),
(7,'Olivia Taylor',34,'開発'),
(8,'Liam Jones',40,'人事'),
(9,'Sophia Anderson',30,'営業'),
(10,'James Moore',27,'開発');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `expenses` (
  `expense_id` int(11) NOT NULL,
  `department` varchar(50) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `unit_price` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `total_cost` int(11) DEFAULT NULL,
  `approved` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`expense_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES
(1,'営業部','名刺印刷',2000,3,6000,0),
(2,'経理部','電卓',1500,2,3000,1),
(3,'開発部','モニター',25000,1,25000,0),
(4,'営業部','ノベルティグッズ',100,100,10000,0),
(5,'人事部','社内研修教材',3000,5,15000,1);
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity_change` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES
(301,1,50),
(302,2,-10),
(303,3,100);
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock_quantity` int(11) NOT NULL DEFAULT 0,
  `status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES
(1,'Phone',80000.00,100,'Active'),
(2,'Laptop',150000.00,50,'Active'),
(3,'Earphones',25000.00,200,'Active');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_initialstate`
--

DROP TABLE IF EXISTS `products_initialstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_initialstate` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock_quantity` int(11) NOT NULL DEFAULT 0,
  `status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_initialstate`
--

LOCK TABLES `products_initialstate` WRITE;
/*!40000 ALTER TABLE `products_initialstate` DISABLE KEYS */;
INSERT INTO `products_initialstate` VALUES
(1,'Phone',80000.00,100,'Active'),
(2,'Laptop',150000.00,50,'Active'),
(3,'Earphones',25000.00,200,'Active');
/*!40000 ALTER TABLE `products_initialstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `progress`
--

DROP TABLE IF EXISTS `progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `progress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_id` int(11) DEFAULT NULL,
  `score` int(11) NOT NULL DEFAULT 0,
  `completed_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `quiz_id` (`quiz_id`),
  CONSTRAINT `progress_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_list` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progress`
--

LOCK TABLES `progress` WRITE;
/*!40000 ALTER TABLE `progress` DISABLE KEYS */;
/*!40000 ALTER TABLE `progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pschool`
--

DROP TABLE IF EXISTS `pschool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pschool` (
  `id` int(11) DEFAULT NULL,
  `category` char(20) DEFAULT NULL,
  `name` char(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pschool`
--

LOCK TABLES `pschool` WRITE;
/*!40000 ALTER TABLE `pschool` DISABLE KEYS */;
INSERT INTO `pschool` VALUES
(1,'Math','Algebra'),
(2,'Science','Philip'),
(3,'History','Tanaka'),
(4,'Language','Smith'),
(5,'Art','Daniel');
/*!40000 ALTER TABLE `pschool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(100) NOT NULL,
  `question_text` text NOT NULL,
  `explanation` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES
(1,'INSERT','INSERT文を使って新しいデータを追加するには？','INSERT文は新しい行を追加するためのSQLです。'),
(2,'UPDATE','既存のデータを変更するにはどのSQL文を使いますか？','UPDATE文は、テーブル内の既存のデータを変更するために使用します。WHERE句を指定しないと全ての行が更新されます。'),
(3,'INSERT','新しい行をusersテーブルに追加する正しいSQL文はどれですか？','INSERT文は新しいデータをテーブルに追加するために使います。列名とVALUESは対応している必要があります。'),
(4,'INSERT','usersテーブルにnameとageを同時に追加する場合の正しい構文はどれですか？','列を複数指定する場合、それに対応する値をVALUESに指定します。'),
(5,'INSERT','INSERT文で全ての列に値を入れる場合、列名の省略は可能ですか？','全ての列に順番通りに値を指定する場合、列名の指定は省略可能です。'),
(6,'INSERT','INSERT文を使って複数行を一度に追加するにはどうすればよいですか？','VALUES句でカンマ区切りにすることで、1つのINSERT文で複数行の追加が可能です。'),
(7,'INSERT','INSERT INTO users VALUES (\"Bob\", 25); がエラーになる可能性があるのはなぜですか？','テーブルのカラム数や順序が異なる場合、省略したINSERT文はエラーになります。列名を明示すると安全です。'),
(8,'delete_single','idが3のデータを削除するSQL文として正しいものは？','DELETE文では必ずFROM句とWHERE句が必要です。正しい構文は「DELETE FROM テーブル名 WHERE 条件」です。'),
(9,'delete_single','名前が \"Taro\" のデータを削除したい。正しいSQLは？','DELETE文では、文字列条件はクォートで囲む必要があります。WHERE句で条件を正しく指定しましょう。'),
(10,'delete_single','DELETE FROM products WHERE price = 0; というSQLの説明として正しいものは？','このSQLは、price列が0であるレコードだけを削除します。'),
(11,'delete_single','WHERE句を省略してDELETE文を実行した場合、何が起こる？','DELETE文でWHERE句を省略すると、条件指定がないためテーブル内の全データが削除されます。注意が必要です。'),
(12,'delete_single','DELETE文を安全に使うために最も重要なことは？','WHERE句を忘れると、すべてのデータが削除される可能性があります。必ず条件を指定しましょう。'),
(13,'delete_multiple','年齢が30歳以上かつステータスが\"active\"のユーザーを削除するSQLはどれか？','複数条件を使うにはANDでつなぎます。文字列の比較はクォートが必要です。'),
(14,'delete_multiple','年齢が20歳未満、または住所がNULLのユーザーを削除するSQLはどれか？','ORを使って複数条件をつなぎます。NULLの比較にはIS NULLを使います。'),
(15,'delete_multiple','次のSQLの意味として正しいものはどれか？ DELETE FROM users WHERE name = \"Ken\" OR age < 18;','WHEREの条件はORでつながれているため、nameが\"Ken\"であるか、ageが18未満のどちらかを満たせば削除されます。'),
(16,'delete_multiple','DELETE FROM users WHERE (age < 20 OR age > 60) AND status = \"inactive\"; に該当するのはどの条件か？','ORとANDを組み合わせる場合、カッコで優先順位を明確にするのが重要です。'),
(17,'delete_multiple','DELETE文で複数条件を指定するときの注意点として正しいものはどれか？','特に複雑な条件の場合、カッコを使って優先順位を明確にする必要があります。'),
(18,'insert_select','INSERT + SELECT 文の目的として正しいものはどれ？','INSERT + SELECT は別のテーブルにデータをコピーするために使います。'),
(19,'insert_select','次のうち正しい INSERT + SELECT 文はどれ？','VALUES句ではなく、SELECT文を使う点に注意。'),
(20,'insert_select','次のSQLの目的は何？\nINSERT INTO new_table (name)\nSELECT name FROM old_table;','old_table の name列の値を new_table にコピーしています。'),
(21,'insert_select','このSQLの誤りはどこ？\nINSERT INTO users (id, name)\nSELECT id FROM customers;','コピー先とコピー元の列数が一致していないためエラーになります。'),
(22,'insert_select','このSQLを実行すると何が起こる？\nINSERT INTO logs (uid, uname)\nSELECT id, name FROM members WHERE age < 18;','条件に合致するデータだけが logs に挿入されます。'),
(23,'insert_select','このSQLは何をしている？\nINSERT INTO archive\nSELECT * FROM orders WHERE status = \'done\';','orders テーブルの完了済みデータを archive にコピーしています。すべての列を一括コピーしています。'),
(24,'UPDATE_SINGLE_COLUMN','商品IDが1の商品の価格を1000に更新するSQL文として正しいものはどれ？','基本的なUPDATE構文の使い方を確認する問題です。'),
(25,'UPDATE_SINGLE_COLUMN','statusが\'inactive\'の商品のstatusを\'active\'に変更するSQL文として正しいものはどれ？','文字列の比較・更新においてシングルクォートが必要である点に注意します。'),
(26,'UPDATE_SINGLE_COLUMN','商品名が「パソコン」の商品の価格を50000に更新する正しいSQL文はどれ？','WHERE句に文字列を使う場合も、シングルクォートで囲む必要があります。'),
(27,'UPDATE_SINGLE_COLUMN','価格が5000円の商品の在庫数を10に変更するSQL文として正しいものはどれ？','WHERE句に数値条件を使ったUPDATE文の典型的な構文です。'),
(28,'UPDATE_SINGLE_COLUMN','在庫数が50の商品のステータスを\'inactive\'に更新するSQL文で正しいものはどれ？','数値を条件にして、文字列を更新するパターンです。構文とクォートに注意しましょう。'),
(29,'UPDATE_MULTIPLE_COLUMNS','次のSQL文は、特定の商品IDの商品名と価格を更新するものです。正しいSQL文はどれですか？','SET句でカンマで区切ることで複数カラムを更新できます。'),
(30,'UPDATE_MULTIPLE_COLUMNS','商品IDが2で、ステータスが\"active\"の商品の在庫と価格を更新したい。正しいSQL文はどれですか？','複数条件はANDで結び、複数カラム更新はSET句でカンマ区切りにします。'),
(31,'UPDATE_MULTIPLE_COLUMNS','productsテーブルで、価格が5000以上でステータスが\"inactive\"の商品のステータスと価格を更新したい。正しいSQLは？','WHERE句には複数条件をANDでつなげ、SETではカンマ区切りで複数カラムの更新をします。'),
(32,'UPDATE_MULTIPLE_COLUMNS','商品IDが3で、現在の在庫数が10の商品について、在庫数とステータスを変更したい。正しいSQLはどれ？','数値条件（=10など）と文字列（ステータス）を正確に記述しましょう。'),
(33,'UPDATE_MULTIPLE_COLUMNS','すべての「在庫数が0かつステータスがinactive」の商品のステータスと在庫数を更新するSQLは？','複数の条件で一致する行に対して、複数カラムを更新する場合の典型的なパターンです。');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_list`
--

DROP TABLE IF EXISTS `quiz_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_name` varchar(255) NOT NULL,
  `total_questions` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `quiz_name` (`quiz_name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_list`
--

LOCK TABLES `quiz_list` WRITE;
/*!40000 ALTER TABLE `quiz_list` DISABLE KEYS */;
INSERT INTO `quiz_list` VALUES
(1,'AVG',5),
(2,'COUNT',5),
(3,'CROSS JOIN',8),
(4,'GROUP BY',10),
(5,'HAVING',10),
(6,'INNER JOIN',8),
(7,'JOIN SAMMARY',10),
(8,'LEFT OUTER JOIN',8),
(9,'MAX',5),
(10,'MIN',5),
(11,'ORDER BY',10),
(12,'RIGHT OUTER JOIN',8),
(13,'SUM',5),
(14,'UPDATE',6),
(15,'INSERT',6),
(16,'DELETE SINGLE',5),
(17,'DELETE MULTIPLE',5),
(18,'INSERT SELECT',6),
(19,'UPDATE SINGLE COLUMN',5),
(20,'UPDATE MULTIPLE COLUMNS',5);
/*!40000 ALTER TABLE `quiz_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result_cities`
--

DROP TABLE IF EXISTS `result_cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `result_cities` (
  `id` char(10) DEFAULT NULL,
  `name` char(30) DEFAULT NULL,
  `population` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result_cities`
--

LOCK TABLES `result_cities` WRITE;
/*!40000 ALTER TABLE `result_cities` DISABLE KEYS */;
INSERT INTO `result_cities` VALUES
('001','Tokyo',13929286),
('002','New York',8419000),
('003','London',8982000),
('004','Paris',2148000),
('005','Berlin',3769000);
/*!40000 ALTER TABLE `result_cities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result_pschool`
--

DROP TABLE IF EXISTS `result_pschool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `result_pschool` (
  `id` int(11) DEFAULT NULL,
  `category` char(20) DEFAULT NULL,
  `name` char(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result_pschool`
--

LOCK TABLES `result_pschool` WRITE;
/*!40000 ALTER TABLE `result_pschool` DISABLE KEYS */;
INSERT INTO `result_pschool` VALUES
(1,'Math','Algebra'),
(2,'Science','Philip'),
(3,'History','Tanaka'),
(4,'Language','Smith'),
(5,'Art','Daniel');
/*!40000 ALTER TABLE `result_pschool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `result_sisya`
--

DROP TABLE IF EXISTS `result_sisya`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `result_sisya` (
  `id` int(11) NOT NULL,
  `year` char(10) DEFAULT NULL,
  `all_died` int(11) DEFAULT NULL,
  `child_died` int(11) DEFAULT NULL,
  `old_died` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `result_sisya`
--

LOCK TABLES `result_sisya` WRITE;
/*!40000 ALTER TABLE `result_sisya` DISABLE KEYS */;
INSERT INTO `result_sisya` VALUES
(1,'2020',100000,5000,30000),
(2,'2021',95000,4500,29000),
(3,'2022',98000,4800,29500),
(4,'2023',92000,4200,28000),
(5,'2019',110000,6000,32000),
(6,'2018',105000,5500,31000),
(7,'2017',108000,5800,31500),
(8,'2016',102000,5200,30500),
(9,'2015',107000,5700,31300);
/*!40000 ALTER TABLE `result_sisya` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales` (
  `id` int(11) NOT NULL,
  `sale_date` date NOT NULL,
  `product_name` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES
(1,'2024-10-01','Apple','Fruit',10,400),
(2,'2024-10-01','Banana','Fruit',20,180),
(3,'2024-10-02','Carrot','Vegetable',15,120),
(4,'2024-10-03','Apple','Fruit',5,420),
(5,'2024-10-04','Potato','Vegetable',30,200),
(6,'2024-10-04','Apple','Fruit',12,415),
(7,'2024-10-05','Orange','Fruit',8,300),
(8,'2024-10-05','Carrot','Vegetable',20,130),
(9,'2024-10-06','Banana','Fruit',18,200),
(10,'2024-10-06','Apple','Fruit',10,450);
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `selected_users`
--

DROP TABLE IF EXISTS `selected_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `selected_users` (
  `selected_id` int(11) NOT NULL,
  `selected_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`selected_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selected_users`
--

LOCK TABLES `selected_users` WRITE;
/*!40000 ALTER TABLE `selected_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `selected_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sisya`
--

DROP TABLE IF EXISTS `sisya`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sisya` (
  `id` int(11) NOT NULL,
  `year` char(10) DEFAULT NULL,
  `all_died` int(11) DEFAULT NULL,
  `child_died` int(11) DEFAULT NULL,
  `old_died` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sisya`
--

LOCK TABLES `sisya` WRITE;
/*!40000 ALTER TABLE `sisya` DISABLE KEYS */;
INSERT INTO `sisya` VALUES
(1,'2020',100000,5000,30000),
(2,'2021',95000,4500,29000),
(3,'2022',98000,4800,29500),
(4,'2023',92000,4200,28000),
(5,'2019',110000,6000,32000),
(6,'2018',105000,5500,31000),
(7,'2017',108000,5800,31500),
(8,'2016',102000,5200,30500),
(9,'2015',107000,5700,31300);
/*!40000 ALTER TABLE `sisya` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team` (
  `team_id` int(11) DEFAULT NULL,
  `name` char(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES
(1,'Team Alpha'),
(2,'Team Bravo'),
(3,'Team Charlie'),
(4,'Team Delta'),
(5,'Team Echo');
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `name` char(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES
(1,1,'Alice'),
(2,1,'Bob'),
(3,2,'Charlie'),
(4,2,'David'),
(5,3,'Eve'),
(6,3,'Frank'),
(7,4,'Grace'),
(8,4,'Hank'),
(9,5,'Ivy'),
(10,5,'Jack');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `age` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'John Doe',30),
(2,'Jane Smith',25),
(3,'Alice Johnson',28),
(4,'Bob Brown',35),
(5,'Charlie Davis',22),
(6,'Emily Evans',27),
(7,'Frank Green',33),
(8,'Grace Harris',24),
(9,'Henry Clark',31),
(10,'Ivy Lewis',29);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-10-21  2:29:16

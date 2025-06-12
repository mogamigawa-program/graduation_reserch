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
(2,'hiroki_db'),
(3,'test_db'),
(8,'5_db'),
(9,'g_db'),
(10,'a_db'),
(11,'b_db'),
(12,'n_db'),
(13,'q_db'),
(14,'f_db'),
(15,'v_db'),
(19,'44_db'),
(20,'55_db'),
(22,'guest_db'),
(23,'guest_1_db'),
(24,'333_db'),
(25,'444_db');
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(2,'hiroki','$2b$12$28UFmsp94RJne.mu/AtbZO5.6BluQEV3iJ13eGvJx7b4LBCHWBr3K'),
(3,'test','$2b$12$bI7HwfWqEz3Rl.LYYFbE4.5rV8d9P.vCKjmmCwQxivXfeSyF.aF.u'),
(7,'4','$2b$12$W0WXMyipeq5Vry3Zpq2E8OiOOMSUFkEOjOpwKMufjLq900vxkVUUK'),
(8,'5','$2b$12$ooYo96T2zVeztgkef9CQ9e1yUIk.zU2QG96SLAxMP3fkXuTKbglWC'),
(9,'g','$2b$12$9qxEk9rCMC3jGkKyFD2EDeVgVmbu71AjoRuKkpZc7PQbTSta7S78S'),
(10,'a','$2b$12$UB8eanT/mqRV8lOYvnF.BuWBSdnlLrjQypQo8y4iTprZpQgVdS/CO'),
(11,'b','$2b$12$.YIZL3PaihlJs.0dlvttBOU14jQdkbxn1yPh0hQhQZZwWlDTKQDpm'),
(12,'n','$2b$12$3rCkE5JxKNLwc15SLbRn9uI3Ngc.1BKhMjXnToj1ugFHivNkhR6Y2'),
(13,'q','$2b$12$sgiCVMrGz/C4T75T129U4eE5jXjzj5ChZXRwLpevfwv.Ps4DkZwVm'),
(14,'f','$2b$12$gDxw/eTnUOUIkaz44s7cL.IA49dOR23tEARA/oTHMNm9PynlLpf7C'),
(15,'v','$2b$12$b0u1r0Sr1BIiimLPc4CCQ.p.KUuLHzcymeKhtuplpb0Rsj.RGC43e'),
(19,'44','$2b$12$GshCxZXikYxf.oaYIy7K6uRhBvJK.n8LPUDJ1W.WAi6enHdyQLKNW'),
(20,'55','$2b$12$wtPuZOiUzrfkI4Rt/a8oXeYx76S2RSQOaHRDdKpHG8VAceB4DBzAq'),
(22,'guest','$2b$12$tQaWr0bKZ3wL96iBVCOou.2RUDQ9tlWWm8bOIckP97RKlHMmwd28i'),
(23,'guest_1','$2b$12$3RATZROHTRtCFbff3Ab7NOtWjbel2S35GZy5R7aZNIKTipO1j2KJW'),
(24,'333','$2b$12$bPqSA3XfQ/9dSPFgsMmAt.ZqzMsre0GwJS1hwFHIKJk0O4o4pe9uu'),
(25,'444','$2b$12$AyoRjcrlim0SrhYAXfwzCusZP6XHdl4G6IqPsMH68e6W0x5SD.QSu');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Current Database: `dataset`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dataset` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `dataset`;

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
  KEY `question_id` (`question_id`),
  CONSTRAINT `choices_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1021 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(1020,17,'複雑な条件では()を使って優先順位を明確にする',1);
/*!40000 ALTER TABLE `choices` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(17,'delete_multiple','DELETE文で複数条件を指定するときの注意点として正しいものはどれか？','特に複雑な条件の場合、カッコを使って優先順位を明確にする必要があります。');
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(17,'DELETE MULTIPLE',5);
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

-- Dump completed on 2025-06-13  3:22:11

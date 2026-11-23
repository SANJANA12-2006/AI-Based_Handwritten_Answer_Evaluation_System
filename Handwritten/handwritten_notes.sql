-- MySQL dump 10.13  Distrib 5.1.61, for Win64 (unknown)
--
-- Host: localhost    Database: handwritten_notes
-- ------------------------------------------------------
-- Server version	5.1.61-community

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
-- Current Database: `handwritten_notes`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `handwritten_notes` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `handwritten_notes`;

--
-- Table structure for table `answer_sheets`
--

DROP TABLE IF EXISTS `answer_sheets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answer_sheets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `submission_id` int(11) NOT NULL,
  `original_filename` varchar(255) NOT NULL,
  `stored_filename` varchar(255) NOT NULL,
  `original_path` varchar(500) NOT NULL,
  `processed_path` varchar(500) DEFAULT NULL,
  `extracted_text` text,
  `page_number` int(11) NOT NULL,
  `processing_status` varchar(30) DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `submission_id` (`submission_id`),
  CONSTRAINT `answer_sheets_ibfk_1` FOREIGN KEY (`submission_id`) REFERENCES `submissions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer_sheets`
--

LOCK TABLES `answer_sheets` WRITE;
/*!40000 ALTER TABLE `answer_sheets` DISABLE KEYS */;
INSERT INTO `answer_sheets` VALUES (1,1,'WhatsApp Image 2026-07-15 at 15.21.56.jpeg','submission_1_3a512f4b90944abf8930b32077801894.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_1_3a512f4b90944abf8930b32077801894.jpeg',NULL,NULL,1,'uploaded','2026-08-15 06:45:36'),(2,2,'java1.jpeg','submission_2_42ab127bddbf4fe7882db1a82e349489.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_2_42ab127bddbf4fe7882db1a82e349489.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\processed\\submission_2_42ab127bddbf4fe7882db1a82e349489_processed.jpg','1 what in Java?\n→ Java is a Interpreted programming Language.\n24 Expand oop?\n→ Object Oriented programming\n34 what is Inheritance?\n→ Inheritance is a process of accening elements\nof one class to another class.',1,'completed','2026-08-15 07:31:18'),(3,3,'java1.jpeg','submission_3_2df06c91bcdb4e5aa0a04cb1a11c1e62.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_3_2df06c91bcdb4e5aa0a04cb1a11c1e62.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\processed\\submission_3_2df06c91bcdb4e5aa0a04cb1a11c1e62_processed.jpg','I what in Java?\n→ Java is a Interpreted programming Language.\n24 Expand oop?\n→ Object Oriented programming\n34 what is Inheritance?\n→ Inheritance is a process of ackening elements\nof one class to another class.',1,'completed','2026-08-15 08:38:23'),(4,4,'java1.jpeg','submission_4_44ca40b46be348ddbe3f499fb7d35bbf.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_4_44ca40b46be348ddbe3f499fb7d35bbf.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\processed\\submission_4_44ca40b46be348ddbe3f499fb7d35bbf_processed.jpg','1 what in Java?\n→ Java is a Interpreted programming Language.\n24 Expand oop?\n→ Object Oriented programming\n34 what is Inheritance?\n→ Inheritance is a process of accessing elements\nof one class to another class.',1,'completed','2026-08-16 08:11:17'),(5,5,'java1.jpeg','submission_5_93e24837aae54e2bb986cae38a594b93.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_5_93e24837aae54e2bb986cae38a594b93.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\processed\\submission_5_93e24837aae54e2bb986cae38a594b93_processed.jpg','I what in Java?\n→ Java is a Interpreted programming Language.\n24 Expand oop?\n→ Object Oriented programming\n34 what is Inheritance?\n→ Inheritance is a process of ackening elements\nof one class to another class.',1,'completed','2026-08-16 08:23:28'),(6,6,'WhatsApp Image 2026-09-01 at 3.56.05 PM.jpeg','submission_6_6483c8c0f6e34bbe9e753896e3f1987e.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_6_6483c8c0f6e34bbe9e753896e3f1987e.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\processed\\submission_6_6483c8c0f6e34bbe9e753896e3f1987e_processed.jpg','Computer Networks',1,'completed','2026-09-01 10:46:50'),(7,7,'WhatsApp Image 2026-09-01 at 4.22.30 PM.jpeg','submission_7_65e834064680449caffeb8f1bfbbd25f.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_7_65e834064680449caffeb8f1bfbbd25f.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\processed\\submission_7_65e834064680449caffeb8f1bfbbd25f_processed.jpg','Computer Networks',1,'completed','2026-09-01 10:53:42'),(8,8,'IMG_20260902_143115603.jpg','submission_8_290ba690982f462db6159d8f4db06d80.jpg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_8_290ba690982f462db6159d8f4db06d80.jpg','F:\\PFS Projects\\Handwritten\\uploads\\processed\\submission_8_290ba690982f462db6159d8f4db06d80_processed.jpg','Computer Networks',1,'completed','2026-09-02 09:07:56'),(9,9,'IMG_20260902_143115603.jpg','submission_9_52517341fb5f4f91808cf619d1277300.jpg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_9_52517341fb5f4f91808cf619d1277300.jpg','F:\\PFS Projects\\Handwritten\\uploads\\processed\\submission_9_52517341fb5f4f91808cf619d1277300_processed.jpg','Computer Networks',1,'completed','2026-09-02 14:26:27'),(10,10,'WhatsApp Image 2026-09-01 at 4.22.30 PM.jpeg','submission_10_28da8b31d44d4e39a0a3c3f4a6a8e383.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\answer_sheets\\submission_10_28da8b31d44d4e39a0a3c3f4a6a8e383.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\processed\\submission_10_28da8b31d44d4e39a0a3c3f4a6a8e383_processed.jpg','Computer Networks',1,'completed','2026-09-02 15:34:47');
/*!40000 ALTER TABLE `answer_sheets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (1,'BCA - 1st Semester','Bachelor of Computer Applications - 1st Semester',NULL),(2,'BCA - 2nd Semester','Bachelor of Computer Applications - 2nd Semester',NULL),(3,'BCA - 3rd Semester','Bachelor of Computer Applications - 3rd Semester',NULL),(4,'BCA - 4th Semester','Bachelor of Computer Applications - 4th Semester',NULL),(5,'BCA - 5th Semester','Bachelor of Computer Applications - 5th Semester',NULL),(6,'BCA - 6th Semester','Bachelor of Computer Applications - 6th Semester',NULL);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluations`
--

DROP TABLE IF EXISTS `evaluations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evaluations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `submission_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `student_answer` text,
  `marks` float DEFAULT NULL,
  `max_marks` float NOT NULL,
  `feedback` text,
  `confidence` float DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `teacher_marks` float DEFAULT NULL,
  `teacher_feedback` text,
  `evaluated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `submission_id` (`submission_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `evaluations_ibfk_1` FOREIGN KEY (`submission_id`) REFERENCES `submissions` (`id`),
  CONSTRAINT `evaluations_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluations`
--

LOCK TABLES `evaluations` WRITE;
/*!40000 ALTER TABLE `evaluations` DISABLE KEYS */;
INSERT INTO `evaluations` VALUES (1,2,1,'Java is a Interpreted programming Language.',5,5,'Excellent answer. The response closely matches the expected answer.',100,'ai_evaluated',NULL,NULL,'2026-08-15 08:08:33'),(2,2,2,'Object Oriented programming',5,5,'Excellent answer. The response closely matches the expected answer.',100,'ai_evaluated',NULL,NULL,'2026-08-15 08:08:33'),(3,2,3,'Inheritance is a process of accening elements\nof one class to another class.',0.91,1,'Excellent answer. The response closely matches the expected answer.',90.96,'ai_evaluated',NULL,NULL,'2026-08-15 08:08:33'),(4,3,1,'',0,5,'No answer was detected for this question.',0,'ai_evaluated',0,'','2026-08-15 08:38:28'),(5,3,2,'Object Oriented programming',5,5,'Excellent answer. The response closely matches the expected answer.',100,'ai_evaluated',5,'','2026-08-15 08:38:35'),(6,3,3,'Inheritance is a process of ackening elements\nof one class to another class.',0.9,1,'Excellent answer. The response closely matches the expected answer.',90,'ai_evaluated',0.9,'','2026-08-15 08:38:35'),(7,4,4,'Java is a Interpreted programming Language.',4.91,5,'Excellent answer. The response closely matches the expected answer.',98.16,'ai_evaluated',4.91,'','2026-08-16 08:11:30'),(8,4,5,'Object Oriented programming\n→ Inheritance is a process of accessing elements\nof one class to another class.',3.23,4,'Good answer. Most important concepts are covered.',80.69,'ai_evaluated',3.23,'','2026-08-16 08:11:31'),(9,5,4,'',0,5,'No answer was detected for this question.',0,'ai_evaluated',NULL,NULL,'2026-08-16 08:23:34'),(10,5,5,'Object Oriented programming\n→ Inheritance is a process of ackening elements\nof one class to another class.',3.29,4,'Good answer. Most important concepts are covered.',82.14,'ai_evaluated',NULL,NULL,'2026-08-16 08:23:34'),(11,8,7,'Computer Networks',5,5,'Excellent answer. The response closely matches the expected answer.',100,'ai_evaluated',5,'','2026-09-02 10:18:31'),(12,9,7,'Computer Networks',5,5,'Excellent answer. The response closely matches the expected answer.',100,'ai_evaluated',5,'','2026-09-02 14:26:41'),(13,10,8,'Computer Networks',5,5,'Excellent answer. The response closely matches the expected answer.',100,'ai_evaluated',5,'','2026-09-02 15:35:01');
/*!40000 ALTER TABLE `evaluations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_id` int(11) NOT NULL,
  `question_number` int(11) NOT NULL,
  `question_text` text NOT NULL,
  `key_answer` text NOT NULL,
  `max_marks` float NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `extracted_text` text,
  `source_filename` varchar(255) DEFAULT NULL,
  `source_path` varchar(500) DEFAULT NULL,
  `source_type` varchar(20) DEFAULT 'text',
  PRIMARY KEY (`id`),
  KEY `test_id` (`test_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`test_id`) REFERENCES `tests` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,1,1,'What is Java?','Java is a interpreted Programming Language.',5,'2026-08-15 06:30:54',NULL,NULL,NULL,'text'),(2,1,2,'Expand OOP?','Object Oriented Programming',5,'2026-08-15 06:31:19',NULL,NULL,NULL,'text'),(3,1,3,'What is Inheritance?','Inheritance is a process of accessing one class elements in another class elements.',1,'2026-08-15 06:31:56',NULL,NULL,NULL,'text'),(4,2,1,'what is java?','java is a interpreted programming language',5,'2026-08-16 08:07:09',NULL,NULL,NULL,'text'),(5,2,2,'explain oop?','object oriented programming',4,'2026-08-16 08:07:55',NULL,NULL,NULL,'text'),(6,3,1,'what is cn?','computer networks',3,'2026-09-01 10:39:04',NULL,NULL,NULL,'text'),(7,4,1,'What is Computer Networks?','Computer Networks',5,'2026-09-02 08:55:43',NULL,NULL,NULL,'text'),(8,5,1,'Computer Networks','Computer Networks',5,'2026-09-02 15:32:45','Computer Networks','WhatsApp Image 2026-09-01 at 3.56.05 PM.jpeg','F:\\PFS Projects\\Handwritten\\uploads\\teacher_questions\\teacher_q_5_a344a659dbdb4e4ea46ff39291cebbcc.jpeg','image');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submissions`
--

DROP TABLE IF EXISTS `submissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `submissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `total_marks` float DEFAULT NULL,
  `percentage` float DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `evaluated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `test_id` (`test_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `submissions_ibfk_1` FOREIGN KEY (`test_id`) REFERENCES `tests` (`id`),
  CONSTRAINT `submissions_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submissions`
--

LOCK TABLES `submissions` WRITE;
/*!40000 ALTER TABLE `submissions` DISABLE KEYS */;
INSERT INTO `submissions` VALUES (1,1,2,NULL,NULL,'uploaded','2026-08-15 06:45:36',NULL),(2,1,3,10.91,99.18,'evaluated','2026-08-15 07:31:18','2026-08-15 08:08:33'),(3,1,4,5.9,53.6364,'teacher_reviewed','2026-08-15 08:38:23','2026-08-15 09:16:00'),(4,2,6,8.14,90.4444,'teacher_reviewed','2026-08-16 08:11:17','2026-08-16 08:15:15'),(5,2,7,3.29,36.56,'evaluated','2026-08-16 08:23:28','2026-08-16 08:23:34'),(6,3,9,NULL,NULL,'completed','2026-09-01 10:46:49',NULL),(7,3,10,NULL,NULL,'completed','2026-09-01 10:53:42',NULL),(8,4,11,5,100,'teacher_reviewed','2026-09-02 09:07:55','2026-09-02 14:31:56'),(9,4,13,5,100,'teacher_reviewed','2026-09-02 14:26:27','2026-09-02 14:31:37'),(10,5,11,5,100,'teacher_reviewed','2026-09-02 15:34:47','2026-09-02 15:35:43');
/*!40000 ALTER TABLE `submissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tests`
--

DROP TABLE IF EXISTS `tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text,
  `duration` int(11) DEFAULT NULL,
  `total_marks` float DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `tests_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tests_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tests`
--

LOCK TABLES `tests` WRITE;
/*!40000 ALTER TABLE `tests` DISABLE KEYS */;
INSERT INTO `tests` VALUES (1,1,3,'Test 1 : Java Fundamentals','This Test is regarding Java Fundamentals.',60,11,'published','2026-08-15 06:30:19'),(2,5,1,'module 1','description',NULL,9,'published','2026-08-16 08:05:33'),(3,8,1,'module 1','',2,3,'published','2026-09-01 10:38:20'),(4,12,4,'Internal 12','Internal 12',10,5,'published','2026-09-02 08:55:18'),(5,12,4,'Internal 13','Internal 13',10,5,'published','2026-09-02 15:18:31');
/*!40000 ALTER TABLE `tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `class_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Asha','asha@gmail.com','7204635947','scrypt:32768:8:1$saU9Mkqj2KztMllN$6e13229cbfa101671ec07d9f3f026965147f2647d833eeff694fadb26e345e47782ddeadcd0195e2c3e60f420e15ddbb50b79d35a773ae9f29cd3d41d98b0c84','teacher',NULL,'2026-08-15 06:22:20','2026-08-15 06:22:20'),(2,'Bhuvan','iambhuvan3@gmail.com','7204635947','scrypt:32768:8:1$UDzJkzNfIgLdjwrp$a682c376acb8771214c92859a7bc7694e4a31f170db993ab0b71137b5a55843a1683730a044ea0c3e4de24f6fb06d573b24b7f11b08e8d89cb2011dc7f59991f','student',3,'2026-08-15 06:23:56','2026-08-15 06:23:56'),(3,'Max','max@gmail.com','7353632618','scrypt:32768:8:1$e68y3OP1r4cbgfU9$9e025fc601d8b9313645d4dfa5d4ffeb7c54dcc3927a21369a8f50751b7adc286735c61094dd0613f7ec6b4e84430fe39677c729edd18e1d7ab65056e7ab971b','student',3,'2026-08-15 07:27:11','2026-08-15 07:27:11'),(4,'Shashank','shashank@gmail.com','9876543210','scrypt:32768:8:1$8azbZqlKIJhzkNfp$14d850dfc06e84f65dc6681aae905b1b4021c2db7bbccf388f07f85ab793b7b30e14ccb526be20fbdec541f8edd3bf98fd716083b3db3cc43ce7db144824a416','student',3,'2026-08-15 08:37:49','2026-08-15 08:37:49'),(5,'apoorva','xyz@gmail.com','','scrypt:32768:8:1$AEBxMcSaYcrYXiZh$294d49747e50f704f99ab1e06e53b1b6228c711b592f201f4d37381bf7a69909c77df8118624b8ef28796a7d910bf2843960ca41b3bafecddba077dcb6fe488b','teacher',NULL,'2026-08-16 08:04:15','2026-08-16 08:04:15'),(6,'druthi','abc@gmail.com','','scrypt:32768:8:1$xr8tWLfyKT76qXoy$9eb5a2f2afc08777de4e1684fefa56ee9832b2197947b588f3090bdb6a80857c27cd5110f9c384d3d54cc3c3cc9ac6dd21c658839835ce4cc68410f306143555','student',1,'2026-08-16 08:10:21','2026-08-16 08:10:21'),(7,'sanju','qwe@gmail.com','','scrypt:32768:8:1$7txDET89UrGtjrZg$6945d5b4a612be4b97fc8b5487e1669ce6a6bebb1cd0ee67a04889bb4d593be15f98954a9bfcee8bcb9da96d3112495e3c3c6f4645467733e9f3dde0000ff592','student',1,'2026-08-16 08:20:16','2026-08-16 08:20:16'),(8,'bhoomi','bhoomi@gmail.com','','scrypt:32768:8:1$s2VBs3RPrHSQapz5$09e216da5ffd618d3e72dae57c02b46272a5960e337e0dff11e3fba4c0d4758cfa5e21571dc077c563b927698bcafd5165f7704543087339dd497f407c1e02d4','teacher',NULL,'2026-09-01 10:37:22','2026-09-01 10:37:22'),(9,'druthi','druthi@gmail.com','','scrypt:32768:8:1$ju8VVitaDhFQnvW3$73e538c71341aadc81d139e3d4bcd7de416d017913eab71798b0a1629b8692a2ff44e2251146ae5058bf1036898c3381284a3cfaf0eaf0ee4fce7d9e58c5020d','student',1,'2026-09-01 10:42:13','2026-09-01 10:42:13'),(10,'sanju','sanju@gmail.com','','scrypt:32768:8:1$oahxgEeadPedGHUO$1a1d44d68100c488edf627619ef4be90a4e00d31480373994de90ce538352e911c275a4ea2fb6fb064f77d1fcbac0b66ac05b8dbaa55d4ba7ab184d5c04e7d05','student',1,'2026-09-01 10:51:17','2026-09-01 10:51:17'),(11,'Anusha','anu@gmail.com','','scrypt:32768:8:1$0f1U1uqNQ692KCzV$9790e981cbd56bb93897469026655575d3ea190776bbc79adb83705266167732ab652e3aab60e388b3e89c532d539c93d847c937e9cf7a3587fb9f100c4deda5','student',4,'2026-09-02 08:33:32','2026-09-02 08:33:32'),(12,'Geetha','geetha@gmail.com','','scrypt:32768:8:1$wAN4kWCbxsHF3RKN$9a4b8c45b887f72d504693ac7bcfbe99cbc57ac1a8190c2032caf8cdfb2779f4bc9e26185a898e25f8e7015c53e17a77b17ae42930ae839b39e2a9d16d9136dc','teacher',NULL,'2026-09-02 08:50:28','2026-09-02 08:50:28'),(13,'iamb1221','iamb1221@gmail.com','','scrypt:32768:8:1$7NnsczMbNMnSSQpD$6160220590c8fc289d57b4f1f71fd22ede02e18abdea6b11794932d86c4e6d912d25a727d659f89cd0a7d0cc92fee2229ec28522d4d20391a5b9e199cf36f929','student',4,'2026-09-02 14:25:54','2026-09-02 14:25:54');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-02 21:18:20

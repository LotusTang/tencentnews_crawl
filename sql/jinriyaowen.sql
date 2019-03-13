/*
 Navicat Premium Data Transfer

 Source Server         : Mysql
 Source Server Type    : MySQL
 Source Server Version : 50627
 Source Host           : localhost:3306
 Source Schema         : tencentnews_data

 Target Server Type    : MySQL
 Target Server Version : 50627
 File Encoding         : 65001

 Date: 13/03/2019 15:48:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for jinriyaowen
-- ----------------------------
DROP TABLE IF EXISTS `jinriyaowen`;
CREATE TABLE `jinriyaowen`  (
  `article_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `url` varchar(70) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`article_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;

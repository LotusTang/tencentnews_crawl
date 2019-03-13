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

 Date: 13/03/2019 15:47:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for newscontent_list_tencent
-- ----------------------------
DROP TABLE IF EXISTS `newscontent_list_tencent`;
CREATE TABLE `newscontent_list_tencent`  (
  `content_id` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `publish_time` datetime(0) NULL DEFAULT NULL,
  `article_content` varchar(21100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  INDEX `content_id`(`content_id`) USING BTREE,
  CONSTRAINT `newscontent_list_tencent_ibfk_1` FOREIGN KEY (`content_id`) REFERENCES `newsurl_list_tencent` (`newsurl_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;

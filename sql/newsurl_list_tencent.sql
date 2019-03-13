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

 Date: 13/03/2019 15:47:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for newsurl_list_tencent
-- ----------------------------
DROP TABLE IF EXISTS `newsurl_list_tencent`;
CREATE TABLE `newsurl_list_tencent`  (
  `newsurl_id` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '新闻标识id',
  `content_id` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '使用此ID去获取原文内容',
  `news_title` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '新闻标题',
  `news_intro` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '新闻简介',
  `keywords` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '关键词',
  `main_category` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '主要分类',
  `sub_category` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '次要分类',
  `comment_id` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '评论id',
  `comment_num` int(8) NULL DEFAULT NULL COMMENT '评论数目',
  `publish_time` datetime(0) NULL DEFAULT NULL COMMENT '发表时间',
  `page_url` varchar(70) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '页面url',
  `source` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '新闻来源',
  `view_count` int(10) NULL DEFAULT NULL COMMENT '阅读数目',
  `is_ztlink` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '是否为专题链接',
  PRIMARY KEY (`newsurl_id`, `content_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;

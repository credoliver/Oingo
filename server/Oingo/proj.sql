/*
 Navicat MySQL Data Transfer

 Source Server         : 3308
 Source Server Type    : MySQL
 Source Server Version : 50723
 Source Host           : localhost:3308
 Source Schema         : proj

 Target Server Type    : MySQL
 Target Server Version : 50723
 File Encoding         : 65001

 Date: 12/12/2018 10:52:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `nid` int(11) NOT NULL,
  `ctext` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `createdBy` int(11) NOT NULL,
  PRIMARY KEY (`cid`) USING BTREE,
  INDEX `nid`(`nid`) USING BTREE,
  INDEX `createdBy`(`createdBy`) USING BTREE,
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`nid`) REFERENCES `note` (`nid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`createdBy`) REFERENCES `user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comment
-- ----------------------------
INSERT INTO `comment` VALUES (1, 1, 'A', 2);
INSERT INTO `comment` VALUES (2, 1, 'B', 3);
INSERT INTO `comment` VALUES (3, 1, 'C', 2);
INSERT INTO `comment` VALUES (4, 1, 'Cool!!!!', 1);
INSERT INTO `comment` VALUES (11, 1, 'sfasd', 3);
INSERT INTO `comment` VALUES (12, 1, 'sfasd', 3);

-- ----------------------------
-- Table structure for filter
-- ----------------------------
DROP TABLE IF EXISTS `filter`;
CREATE TABLE `filter`  (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `ffrom` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `ftag` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `flongi` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `flati` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `fradius` int(11) NULL DEFAULT NULL,
  `fuid` int(11) NULL DEFAULT NULL,
  `fsid` int(11) NULL DEFAULT NULL,
  `ftime` datetime(0) NULL DEFAULT NULL,
  `fstate` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`fid`) USING BTREE,
  INDEX `fuid_fk`(`fuid`) USING BTREE,
  INDEX `filter_ibfk_1`(`fsid`) USING BTREE,
  CONSTRAINT `filter_ibfk_1` FOREIGN KEY (`fsid`) REFERENCES `schedule` (`sid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fuid_fk` FOREIGN KEY (`fuid`) REFERENCES `user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of filter
-- ----------------------------
INSERT INTO `filter` VALUES (1, 'self', '#TS', '121', '121', 10, 3, 4, '2018-12-11 19:26:04', 'Boring');
INSERT INTO `filter` VALUES (2, 'all', '#DB', '-73.982861', '40.696173', 10, 3, 1, '2018-12-11 12:56:58', 'CSing');

-- ----------------------------
-- Table structure for friend
-- ----------------------------
DROP TABLE IF EXISTS `friend`;
CREATE TABLE `friend`  (
  `uid1` int(11) NOT NULL,
  `uid2` int(11) NOT NULL,
  PRIMARY KEY (`uid1`, `uid2`) USING BTREE,
  INDEX `uid2_fk`(`uid2`) USING BTREE,
  CONSTRAINT `uid1_fk` FOREIGN KEY (`uid1`) REFERENCES `user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `uid2_fk` FOREIGN KEY (`uid2`) REFERENCES `user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of friend
-- ----------------------------
INSERT INTO `friend` VALUES (1, 2);
INSERT INTO `friend` VALUES (3, 2);
INSERT INTO `friend` VALUES (1, 3);
INSERT INTO `friend` VALUES (3, 7);

-- ----------------------------
-- Table structure for friendrequest
-- ----------------------------
DROP TABLE IF EXISTS `friendrequest`;
CREATE TABLE `friendrequest`  (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `ruid1` int(11) NOT NULL,
  `ruid2` int(11) NOT NULL,
  PRIMARY KEY (`rid`) USING BTREE,
  INDEX `ruid_fk`(`ruid1`) USING BTREE,
  INDEX `ruid2`(`ruid2`) USING BTREE,
  CONSTRAINT `friendrequest_ibfk_1` FOREIGN KEY (`ruid2`) REFERENCES `user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ruid_fk` FOREIGN KEY (`ruid1`) REFERENCES `user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of friendrequest
-- ----------------------------
INSERT INTO `friendrequest` VALUES (1, 2, 3);
INSERT INTO `friendrequest` VALUES (2, 1, 3);
INSERT INTO `friendrequest` VALUES (4, 7, 3);

-- ----------------------------
-- Table structure for note
-- ----------------------------
DROP TABLE IF EXISTS `note`;
CREATE TABLE `note`  (
  `nid` int(11) NOT NULL AUTO_INCREMENT,
  `ntext` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ntime` datetime(0) NOT NULL,
  `nlongi` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `nlati` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `nradius` int(11) NOT NULL,
  `nsid` int(11) NULL DEFAULT NULL,
  `createdBy` int(11) NOT NULL,
  `visibility` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `commentable` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`nid`) USING BTREE,
  INDEX `cretedBy`(`createdBy`) USING BTREE,
  INDEX `sid_fk`(`nsid`) USING BTREE,
  CONSTRAINT `cretedBy` FOREIGN KEY (`createdBy`) REFERENCES `user` (`uid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sid_fk` FOREIGN KEY (`nsid`) REFERENCES `schedule` (`sid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of note
-- ----------------------------
INSERT INTO `note` VALUES (1, 'A', '2018-12-11 10:21:50', '-73.983345', '40.695872', 60, 3, 3, 'all', '1');
INSERT INTO `note` VALUES (2, 'B', '2018-12-11 09:11:15', '-73.983345', '40.695872', 100, 1, 3, 'friend', '0');
INSERT INTO `note` VALUES (3, 'C  ', '2018-12-11 09:12:20', '-73.983345', '40.695872', 200, 1, 2, 'self', '1');
INSERT INTO `note` VALUES (10, 'Thanks TS!', '2018-12-01 11:08:19', '123', '31', 100, 12, 1, 'all', '1');
INSERT INTO `note` VALUES (14, 'Fuck TS!', '2018-12-11 11:08:19', '123', '31', 100, 16, 2, 'all', '1');

-- ----------------------------
-- Table structure for notetag
-- ----------------------------
DROP TABLE IF EXISTS `notetag`;
CREATE TABLE `notetag`  (
  `tname` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `nid` int(11) NOT NULL,
  PRIMARY KEY (`tname`, `nid`) USING BTREE,
  INDEX `notetag_ibfk_1`(`nid`) USING BTREE,
  CONSTRAINT `notetag_ibfk_1` FOREIGN KEY (`nid`) REFERENCES `note` (`nid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notetag
-- ----------------------------
INSERT INTO `notetag` VALUES ('#DB', 1);
INSERT INTO `notetag` VALUES ('#DB', 2);
INSERT INTO `notetag` VALUES ('#DB', 3);
INSERT INTO `notetag` VALUES ('#DB', 10);
INSERT INTO `notetag` VALUES ('#DB', 14);

-- ----------------------------
-- Table structure for schedule
-- ----------------------------
DROP TABLE IF EXISTS `schedule`;
CREATE TABLE `schedule`  (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `starttime` datetime(0) NULL DEFAULT NULL,
  `endtime` datetime(0) NULL DEFAULT NULL,
  `repetition` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`sid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of schedule
-- ----------------------------
INSERT INTO `schedule` VALUES (1, '2018-12-11 13:41:33', '2018-12-25 13:39:08', 4);
INSERT INTO `schedule` VALUES (3, '2018-12-11 13:41:28', '2018-12-25 13:39:10', 4);
INSERT INTO `schedule` VALUES (4, '2018-12-01 10:08:19', '2018-12-25 10:08:19', 10);
INSERT INTO `schedule` VALUES (12, '2018-12-01 10:08:19', '2018-12-25 10:08:19', 4);
INSERT INTO `schedule` VALUES (16, '2018-12-01 10:08:19', '2018-12-30 10:08:19', 0);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `uemail` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `upassword` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ustate` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `ulongi` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `ulati` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `ucurrentTime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'FK', 'FK2469@outlook.com', '123456', 'CSing', '-73.982861', '40.696173', '2018-12-11 19:18:24');
INSERT INTO `user` VALUES (2, 'A', 'A', 'A', 'A', '-73.982861', '40.696173', '2018-12-11 19:18:39');
INSERT INTO `user` VALUES (3, 'b', 'b', 'b', 'CSing', '-73.982861', '40.696173', '2018-12-25 11:08:19');
INSERT INTO `user` VALUES (7, 'c', 'FK@outlook.com', 'c', 'A', '-73.982860', '40.696173', '2018-12-11 19:19:18');

-- ----------------------------
-- View structure for activedfilter
-- ----------------------------
DROP VIEW IF EXISTS `activedfilter`;
CREATE ALGORITHM = UNDEFINED DEFINER = `root`@`localhost` SQL SECURITY DEFINER VIEW `activedfilter` AS select distinct `f`.`fid` AS `fid`,`f`.`ffrom` AS `ffrom`,`f`.`ftag` AS `ftag`,`f`.`fuid` AS `fuid`,`f`.`fstate` AS `fstate` from ((`user` join `filter` `f` on((`user`.`uid` = `f`.`fuid`))) join `schedule` `s2` on((`s2`.`sid` = `f`.`fsid`))) where (((`user`.`ucurrentTime` <> NULL) and (`user`.`ucurrentTime` between `s2`.`starttime` and `s2`.`endtime`)) or ((`user`.`ucurrentTime` = NULL) and (now() between `s2`.`starttime` and `s2`.`endtime`) and (`s2`.`repetition` = NULL)) or ((conv(`s2`.`repetition`,10,2) & conv((1 << (dayofweek(now()) - 1)),10,2)) and (round((((6378.137 * 2) * asin(sqrt((pow(sin((((`f`.`flati` - `user`.`ulati`) * pi()) / 360)),2) + ((cos(((`f`.`flati` * pi()) / 180)) * cos((((`user`.`ulati` + 0.0) * pi()) / 180))) * pow(sin((((`f`.`flongi` - `user`.`ulongi`) * pi()) / 360)),2)))))) * 1000),0) <= `f`.`fradius`)));

-- ----------------------------
-- View structure for activednotes
-- ----------------------------
DROP VIEW IF EXISTS `activednotes`;
CREATE ALGORITHM = UNDEFINED DEFINER = `root`@`localhost` SQL SECURITY DEFINER VIEW `activednotes` AS select distinct `user`.`uid` AS `uid`,`note`.`nid` AS `nid`,`note`.`createdBy` AS `nBelong` from ((`user` join `note`) join `schedule`) where (((`user`.`ucurrentTime` <> NULL) and (`user`.`ucurrentTime` between `schedule`.`starttime` and `schedule`.`endtime`)) or ((`user`.`ucurrentTime` = NULL) and (now() between `schedule`.`starttime` and `schedule`.`endtime`) and (`schedule`.`repetition` = NULL)) or ((conv(`schedule`.`repetition`,10,2) & conv((1 << (dayofweek(now()) - 1)),10,2)) and (round((((6378.137 * 2) * asin(sqrt((pow(sin((((`note`.`nlati` - `user`.`ulati`) * pi()) / 360)),2) + ((cos(((`note`.`nlati` * pi()) / 180)) * cos((((`user`.`ulati` + 0.0) * pi()) / 180))) * pow(sin((((`note`.`nlongi` - `user`.`ulongi`) * pi()) / 360)),2)))))) * 1000),0) <= `note`.`nradius`) and (`note`.`visibility` = 'all')) or ((`note`.`visibility` = 'friend ') and `user`.`uid` in (select `friend`.`uid2` from `friend` where (`friend`.`uid1` = `note`.`createdBy`) union all select `friend`.`uid1` from `friend` where (`friend`.`uid2` = `note`.`createdBy`))) or ((`note`.`visibility` = 'self') and (`note`.`createdBy` = `user`.`uid`)));

-- ----------------------------
-- View structure for applyfilter
-- ----------------------------
DROP VIEW IF EXISTS `applyfilter`;
CREATE ALGORITHM = UNDEFINED DEFINER = `root`@`localhost` SQL SECURITY DEFINER VIEW `applyfilter` AS select distinct `an`.`uid` AS `uid`,`an`.`nid` AS `nid` from (((`activednotes` `an` join `activedfilter` `f` on((`an`.`uid` = `f`.`fuid`))) join `note` `n` on(((`an`.`nid` = `n`.`nid`) and `f`.`ftag` in (select `notetag`.`tname` from `notetag` where (`an`.`nid` = `notetag`.`nid`))))) join `user` `u` on((`an`.`uid` = `u`.`uid`))) where (((`f`.`fstate` = `u`.`ustate`) and (`f`.`ffrom` = 'all')) or ((`f`.`ffrom` = 'friend') and `an`.`nBelong` in (select `friend`.`uid2` from `friend` where (`friend`.`uid1` = `an`.`uid`) union all select `friend`.`uid1` from `friend` where (`friend`.`uid2` = `an`.`uid`))) or ((`f`.`ffrom` = 'self') and (`an`.`uid` = `an`.`nBelong`)));

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `spider_json` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `brand` varchar(20) DEFAULT NULL COMMENT '品牌',
 `series` varchar(30) DEFAULT NULL COMMENT '车系',
 `models` varchar(100) DEFAULT NULL COMMENT '车型',
 `guide_price` varchar(20) DEFAULT NULL COMMENT '指导价',
 `level` varchar(10) DEFAULT NULL COMMENT '级别',
 `emission_standard` varchar(20) DEFAULT NULL COMMENT '环保标准',
 `structure` varchar(15) DEFAULT NULL COMMENT '车身结构',
 `status` varchar(10) DEFAULT NULL COMMENT '状态',
 `manufacturer` varchar(20) DEFAULT NULL COMMENT '厂商',
 `year` int(11) DEFAULT NULL COMMENT '年款',
 `font_letter` varchar(5) DEFAULT NULL COMMENT '开头字母',
 `json_text` text COMMENT 'json',
 `url` varchar(200) DEFAULT NULL,
 `spaceid` int(10) DEFAULT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15114 DEFAULT CHARSET=utf8
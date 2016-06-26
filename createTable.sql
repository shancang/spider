CREATE TABLE `spider`.`spider_json` (
     `id` INT (10) NOT NULL ,
     `spaceid` INT (10) NULL DEFAULT NULL,
     `brand` VARCHAR (20) NULL DEFAULT NULL COMMENT '品牌',
     `series` VARCHAR (30) NULL DEFAULT NULL COMMENT '车系',
     `models` VARCHAR (50) NULL DEFAULT NULL COMMENT '车型',
     `guide_price` VARCHAR (20) NULL DEFAULT NULL COMMENT '指导价',
     `level` VARCHAR (10) NULL DEFAULT NULL COMMENT '级别',
     `emission_standard` VARCHAR (10) NULL DEFAULT NULL COMMENT '环保标准',
     `structure` VARCHAR (10) NULL DEFAULT NULL COMMENT '车身结构',
     `status` VARCHAR (10) NULL DEFAULT NULL COMMENT '状态',
     `manufacturer` VARCHAR (20) NULL DEFAULT NULL COMMENT '厂商',
     `json_text` TEXT NULL DEFAULT NULL COMMENT 'json',
     `url` VARCHAR (200) NULL DEFAULT NULL
) ENGINE = INNODB;
alter table spider_json change id id int not null auto_increment primary key;

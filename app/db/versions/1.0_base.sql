CREATE TABLE `cards` (
	`id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '교통카드 ID',
	`name` varchar(32) NOT NULL COMMENT '교통카드 명',
	`max_count` int COMMENT '최대 적립 횟수',
	`min_count` int COMMENT '최소 이용 횟수',
	`youth_age` int COMMENT '청년 기준 나이',
	`senior_age` int COMMENT '우대 나이',
	`min_cost` int NOT NULL DEFAULT 0 COMMENT '최소 지불 금액',
	`adult` int COMMENT '일반 할인율',
	`youth` int COMMENT '청년 할인율',
	`low` int COMMENT '저소득층 할인율',
	`senior` int COMMENT '경로 할인율',
	`location_id`int unsigned COMMENT '지역 ID',
	`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    `removed_at` timestamp NULL DEFAULT NULL COMMENT '삭제일시',
	PRIMARY KEY (`id`),
	KEY `cards_fk_1` (`location_id`),
    CONSTRAINT `cards_fk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`)
	) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '교통카드 종류';


CREATE TABLE `locations` (
	`id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '지역 ID',
	`name` varchar(32) NOT NULL COMMENT '지역 명',
	PRIMARY KEY (`id`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '지역(시/도)';


INSERT INTO `locations`(`name`) VALUES ('서울'), ('경기'), ('인천'), ('기타');


INSERT INTO `cards`(`name`, `max_count`, `min_count`,`youth_age`,`min_cost`, `adult`, `youth`,`low`,`senior`,`location_id`)
VALUES  ('K-패스', 60, 15, 34, 0, 20, 30, 53, 20, 4),
		('인천I패스', NULL, 15, 39, 0, 20, 30, 53, 30,3),
		('The경기패스', NULL, 15, 39, 0,20, 30, 53, 20, 2),
		('기후동행카드', NULL, NULL, 34, 62000, 0, 7000, 0, 0, 1);

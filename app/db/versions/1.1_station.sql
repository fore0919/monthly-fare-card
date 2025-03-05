
CREATE TABLE `stations` (
    `id` INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '지하철 역 id',
    `station_name` VARCHAR(255) NOT NULL COMMENT '지하철 역명',
    `is_departure_allowed` BOOLEAN DEFAULT TRUE COMMENT '기후동행 승차가능역',
    `is_arrival_allowed` BOOLEAN DEFAULT TRUE COMMENT '기후동행 하차가능역'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '지하철역';


CREATE TABLE `lines` (
    `id` INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '노선 id',
    `line_name` VARCHAR(255) NOT NULL COMMENT '노선명',
    `operator` VARCHAR(255) NOT NULL COMMENT '운영기관'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '노선';


CREATE TABLE `station_line` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `station_id` INT NOT NULL,
    `line_id` INT NOT NULL,
    `sequence` INT NOT NULL COMMENT '역순서',
    `distance_from_prev` DECIMAL(5,2) DEFAULT NULL COMMENT '이전역간 거리',
    CONSTRAINT `fk_station` FOREIGN KEY (`station_id`) REFERENCES `stations`(`id`),
    CONSTRAINT `fk_line` FOREIGN KEY (`line_id`) REFERENCES `lines`(`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '노선정보';
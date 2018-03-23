CREATE DATABASE IF NOT EXISTS dm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE reg_db (
  id          INT(11)      NOT NULL AUTO_INCREMENT,
  type        VARCHAR(30) NOT NULL,
  name        VARCHAR(30) NOT NULL,
  db_info     TEXT        NOT NULL,
  created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  updated_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE task (
  id             INT(11)      NOT NULL  AUTO_INCREMENT,
  db_id          INT(11)      NOT NULL,
  table_name     VARCHAR(128) NOT NULL,
  sql_sentence   TEXT         NOT NULL,
  periodic_time  FLOAT        NOT NULL DEFAULT '0',
  next_exec_time DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  exec_times     INT(11)      NOT NULL DEFAULT '0',
  exec_type      TINYINT(2)   NOT NULL COMMENT '0:不周期执行 1:周期执行',
  exec_status    TINYINT(2)   NOT NULL DEFAULT '0' COMMENT '0:任务等待执行 1:任务正在执行',
  status         TINYINT(2)   NOT NULL COMMENT '0:停止的task 1:有效task',
  created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  updated_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT t_db_id FOREIGN KEY (db_id) REFERENCES reg_db (id)
);

CREATE TABLE reg_db_data (
  id             INT(11)      NOT NULL AUTO_INCREMENT,
  db_id          INT(11)      NOT NULL,
  table_name     VARCHAR(128) NOT NULL,
  data           TEXT         NOT NULL,
  created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT d_db_id FOREIGN KEY (db_id) REFERENCES reg_db (id)
);

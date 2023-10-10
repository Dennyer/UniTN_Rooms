CREATE DATABASE IF NOT EXISTS uni;

USE uni;

CREATE TABLE IF NOT EXISTS userdata (
  id VARCHAR(50) NOT NULL, /*User ID*/
  PRIMARY KEY (id)
) Engine = InnoDB default charset = utf8mb4 collate = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS headquarter (
  id VARCHAR(50) NOT NULL, /*User ID*/
  name_headquarter VARCHAR(255) NOT NULL, /*Headquarter name*/
  code VARCHAR(255) NOT NULL, /*Headquarter code*/
  PRIMARY KEY (id, code),
  FOREIGN KEY (id) REFERENCES userdata(Id)
) Engine = InnoDB default charset = utf8mb4 collate = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS course (
  id VARCHAR(50) NOT NULL, /*User ID*/
  course VARCHAR(255) NOT NULL, /*Course name*/
  course_year INT NOT NULL, /*Year of course*/
  PRIMARY KEY (id, course, course_year),
  FOREIGN KEY (id) REFERENCES userdata(Id)
) Engine = InnoDB default charset = utf8mb4 collate = utf8mb4_unicode_ci;

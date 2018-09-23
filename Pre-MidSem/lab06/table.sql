-- DROP database 150123046_23feb2018;

create database 150123046_23feb2018;
use 150123046_23feb2018;

-- drop table ett;
-- drop table cc;
-- drop table cwsl;

CREATE TABLE ett (line_number INTEGER, course_id VARCHAR(20) NOT NULL, exam_date DATE NOT NULL, start_time TIME NOT NULL, end_time TIME NOT NULL,
	CHECK (
		(((start_time >= '09:00:00') AND (start_time <= '12:00:00')) AND ((end_time >= '09:00:00') AND (end_time <= '12:00:00')) AND (start_time < end_time)) 
		OR 
		(((start_time >= '14:00:00') AND (start_time <= '17:00:00')) AND (((end_time >= '14:00:00') AND (end_time <= '17:00:00')))  AND (start_time < end_time))
		), 
	PRIMARY KEY (course_id, exam_date, start_time));
CREATE TABLE cc (course_id VARCHAR(20) NOT NULL, number_of_credits INTEGER NOT NULL CHECK (number_of_credits >= 0), PRIMARY KEY (course_id));
CREATE TABLE cwsl (serial_number INTEGER, roll_number VARCHAR(20) NOT NULL, name VARCHAR(50) NULL, email VARCHAR(50) NULL, course_id VARCHAR(20) NOT NULL, PRIMARY KEY (roll_number, course_id));


-- DROP database 150123046_23feb2018;

-- LOAD DATA LOCAL INFILE 'ett.csv' INTO TABLE ett FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
-- LOAD DATA LOCAL INFILE 'cc.csv' INTO TABLE cc FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
-- LOAD DATA LOCAL INFILE 'cwsl.csv' INTO TABLE cwsl FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';

source 150123046_ett.sql;
source 150123046_cc.sql;
source 150123046_cwsl.sql;

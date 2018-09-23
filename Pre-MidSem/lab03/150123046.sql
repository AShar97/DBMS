#DROP database 25jan2018;

create database 25jan2018;
use 25jan2018;

/*drop table ett;
drop table ett_temp;
drop table ett_clone;

drop table cc;
drop table cc_temp;
drop table cc_clone;

drop table cwsl;
drop table cwsl_temp;
drop table cwsl_clone;*/

CREATE TABLE ett (course_id VARCHAR(20) NOT NULL, exam_date DATE NOT NULL, start_time TIME NOT NULL, end_time TIME NOT NULL,
	CHECK (
		(((start_time >= '09:00:00') AND (start_time <= '12:00:00')) AND ((end_time >= '09:00:00') AND (end_time <= '12:00:00')) AND (start_time < end_time)) 
		OR 
		(((start_time >= '14:00:00') AND (start_time <= '17:00:00')) AND (((end_time >= '14:00:00') AND (end_time <= '17:00:00')))  AND (start_time < end_time))
		), 
	PRIMARY KEY (course_id, exam_date, start_time));
CREATE TABLE cc (course_id VARCHAR(20) NOT NULL, number_of_credits INTEGER NOT NULL CHECK (number_of_credits > 0), PRIMARY KEY (course_id));
CREATE TABLE cwsl (cid VARCHAR(20) NOT NULL, serial_number INTEGER, roll_number VARCHAR(20) NOT NULL, name VARCHAR(50) NULL, email VARCHAR(50) NULL, PRIMARY KEY (cid, roll_number));

CREATE TEMPORARY TABLE ett_temp (course_id VARCHAR(20) NOT NULL, exam_date DATE NOT NULL, start_time TIME NOT NULL, end_time TIME NOT NULL,
	CHECK (
		(((start_time >= '09:00:00') AND (start_time <= '12:00:00')) AND ((end_time >= '09:00:00') AND (end_time <= '12:00:00')) AND (start_time < end_time)) 
		OR 
		(((start_time >= '14:00:00') AND (start_time <= '17:00:00')) AND (((end_time >= '14:00:00') AND (end_time <= '17:00:00')))  AND (start_time < end_time))
		), 
	PRIMARY KEY (course_id, exam_date, start_time));
CREATE TEMPORARY TABLE cc_temp (course_id VARCHAR(20) NOT NULL, number_of_credits INTEGER NOT NULL, PRIMARY KEY (course_id));
CREATE TEMPORARY TABLE cwsl_temp (cid VARCHAR(20) NOT NULL, serial_number INTEGER, roll_number VARCHAR(20) NOT NULL, name VARCHAR(50) NULL, email VARCHAR(50) NULL, PRIMARY KEY (cid, roll_number));

CREATE TABLE ett_clone LIKE ett;
CREATE TABLE cc_clone LIKE cc;
CREATE TABLE cwsl_clone LIKE cwsl;

#DROP database 25jan2018;

/*
source 150123046_ett.sql;
source 150123046_cc.sql;
source 150123046_cwsl.sql;
*/
